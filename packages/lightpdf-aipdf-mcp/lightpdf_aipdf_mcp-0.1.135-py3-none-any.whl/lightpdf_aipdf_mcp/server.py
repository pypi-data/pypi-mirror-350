"""LightPDF Agent MCP Server模块"""
# 标准库导入
import asyncio
import os
import sys
import argparse
import json
from typing import List, Dict, Any, Callable, TypeVar, Optional, Union

# 第三方库导入
from dotenv import load_dotenv

# MCP相关导入
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

# 本地导入
from .common import BaseResult, Logger, FileHandler
from .converter import Converter, ConversionResult
from .editor import Editor, EditResult, EditType
from .translator import Translator, TranslateResult

# 加载环境变量
load_dotenv()

# 类型定义
T = TypeVar('T', bound=BaseResult)
ProcessFunc = Callable[[str], Any]

def generate_result_report(
    results: List[BaseResult]
) -> str:
    """生成通用结果报告
    
    Args:
        results: 结果列表
        
    Returns:
        str: JSON格式的报告文本
    """
    # 统计结果
    success_count = sum(1 for r in results if r.success)
    failed_count = len(results) - success_count
    
    # 构建结果JSON对象
    report_obj = {
        "total": len(results),
        "success_count": success_count,
        "failed_count": failed_count,
        "success_files": [],
        "failed_files": []
    }
    
    for result in results:
        if result.success:
            # 添加成功的文件信息
            report_obj["success_files"].append({
                "download_url": result.download_url,
                "original_name": result.original_name,
                "debug": {
                    "task_id": result.task_id
                }
            })
        else:
            # 添加失败的文件信息
            report_obj["failed_files"].append({
                "error_message": result.error_message,
                "original_name": result.original_name,
                "debug": {
                    "task_id": result.task_id
                }
            })
    
    # 返回JSON字符串
    return json.dumps(report_obj, ensure_ascii=False)

async def process_batch_files(
    file_objects: List[Dict[str, str]], 
    logger: Logger, 
    process_func: Callable[[str, Optional[str], Optional[str]], T],
    operation_desc: Optional[str] = None
) -> List[T]:
    """通用批处理文件函数
    
    Args:
        file_objects: 文件对象列表，每个对象包含path和可选的password及name
        logger: 日志记录器
        process_func: 处理单个文件的异步函数，接收file_path、password和original_name参数
        operation_desc: 操作描述，用于日志记录
    
    Returns:
        List[T]: 处理结果列表
    """
    if len(file_objects) > 1 and operation_desc:
        await logger.log("info", f"开始批量{operation_desc}，共 {len(file_objects)} 个文件")
        
        # 并发处理文件，限制并发数为2
        semaphore = asyncio.Semaphore(6)
        
        async def process_with_semaphore(file_obj: Dict[str, str]) -> T:
            async with semaphore:
                file_path = file_obj["path"]
                password = file_obj.get("password")
                original_name = file_obj.get("name")
                return await process_func(file_path, password, original_name)
        
        # 创建任务列表
        tasks = [process_with_semaphore(file_obj) for file_obj in file_objects]
        return await asyncio.gather(*tasks)
    else:
        # 单文件处理
        file_path = file_objects[0]["path"]
        password = file_objects[0].get("password")
        original_name = file_objects[0].get("name")
        return [await process_func(file_path, password, original_name)]

async def process_conversion_file(
    file_path: str, 
    format: str, 
    converter: Converter, 
    extra_params: Optional[Dict[str, Any]] = None, 
    password: Optional[str] = None,
    original_name: Optional[str] = None
) -> ConversionResult:
    """处理单个文件转换"""
    is_page_numbering = format == "number-pdf"
    
    if is_page_numbering and extra_params:
        # 对于添加页码，使用add_page_numbers方法
        return await converter.add_page_numbers(
            file_path, 
            extra_params.get("start_num", 1),
            extra_params.get("position", "5"),
            extra_params.get("margin", 30),
            password,
            original_name
        )
    else:
        # 处理extra_params
        if extra_params is None:
            extra_params = {}
        # 直接传递 merge_all 参数（如有）
        # 其它逻辑交由 converter.convert_file 处理
        return await converter.convert_file(file_path, format, extra_params, password, original_name)

async def process_edit_file(
    file_path: str, 
    edit_type: str, 
    editor: Editor, 
    extra_params: Dict[str, Any] = None,
    password: Optional[str] = None,
    original_name: Optional[str] = None
) -> EditResult:
    """处理单个文件编辑"""
    if edit_type == "decrypt":
        return await editor.decrypt_pdf(file_path, password, original_name)
    elif edit_type == "add_text_watermark":
        return await editor.add_text_watermark(
            file_path=file_path,
            text=extra_params.get("text", "文本水印"),
            position=extra_params.get("position", "center"),
            opacity=extra_params.get("opacity", 1.0),
            range=extra_params.get("range", ""),
            layout=extra_params.get("layout", "on"),
            font_family=extra_params.get("font_family"),
            font_size=extra_params.get("font_size"),
            font_color=extra_params.get("font_color"),
            password=password,
            original_name=original_name
        )
    elif edit_type == "add_image_watermark":
        return await editor.add_image_watermark(
            file_path=file_path,
            image_url=extra_params.get("image_url"),
            position=extra_params.get("position", "center"),
            opacity=extra_params.get("opacity", 0.7),
            range=extra_params.get("range", ""),
            layout=extra_params.get("layout", "on"),
            password=password,
            original_name=original_name
        )
    elif edit_type == "encrypt":
        return await editor.encrypt_pdf(
            file_path=file_path,
            password=extra_params.get("password", ""),
            provider=extra_params.get("provider", ""),
            original_password=password,
            original_name=original_name
        )
    elif edit_type == "compress":
        return await editor.compress_pdf(
            file_path=file_path,
            image_quantity=extra_params.get("image_quantity", 60),
            password=password,
            original_name=original_name
        )
    elif edit_type == "split":
        return await editor.split_pdf(
            file_path=file_path,
            pages=extra_params.get("pages", ""),
            password=password,
            split_type=extra_params.get("split_type", "page"),
            merge_all=extra_params.get("merge_all", 1),
            original_name=original_name
        )
    elif edit_type == "merge":
        # 对于合并操作，我们需要特殊处理，因为它需要处理多个文件
        return EditResult(
            success=False, 
            file_path=file_path, 
            error_message="合并操作需要使用特殊处理流程",
            original_name=original_name
        )
    elif edit_type == "rotate":
        # 从extra_params获取旋转参数列表
        rotation_arguments = extra_params.get("rotates", [])
        
        # 验证旋转参数列表
        if not rotation_arguments:
            return EditResult(
                success=False, 
                file_path=file_path, 
                error_message="旋转操作需要至少提供一个旋转参数",
                original_name=original_name
            )
        
        # 构建angle_params字典: {"90": "2-4,6-8", "180": "all"}
        angle_params = {}
        for arg in rotation_arguments:
            angle = str(arg.get("angle", 90))
            pages = arg.get("pages", "all") or "all"  # 确保空字符串转为"all"
            angle_params[angle] = pages
        
        # 直接调用rotate_pdf方法，传入角度参数字典
        return await editor.rotate_pdf(
            file_path=file_path,
            angle_params=angle_params,
            password=password,
            original_name=original_name
        )
    elif edit_type == "remove_margin":
        # 直接调用remove_margin方法，不需要额外参数
        return await editor.remove_margin(
            file_path=file_path,
            password=password,
            original_name=original_name
        )
    elif edit_type == "extract_image":
        # 调用extract_images方法提取图片
        return await editor.extract_images(
            file_path=file_path,
            format=extra_params.get("format", "png"),
            password=password,
            original_name=original_name
        )
    else:
        return EditResult(
            success=False, 
            file_path=file_path, 
            error_message=f"不支持的编辑类型: {edit_type}",
            original_name=original_name
        )

async def process_tool_call(
    logger: Logger, 
    file_objects: List[Dict[str, str]], 
    operation_config: Dict[str, Any]
) -> types.TextContent:
    """通用工具调用处理函数
    
    Args:
        logger: 日志记录器
        file_objects: 文件对象列表，每个对象包含path和可选的password
        operation_config: 操作配置，包括操作类型、格式、参数等
        
    Returns:
        types.TextContent: 包含处理结果的文本内容
    """
    file_handler = FileHandler(logger)
    editor = Editor(logger, file_handler)
    extra_params = operation_config.get("extra_params", {})

    # 新增：翻译操作分支
    if operation_config.get("is_translate_operation"):
        translator = Translator(logger, file_handler)

        results = await process_batch_files(
            file_objects,
            logger,
            lambda file_path, password, original_name: translator.translate_pdf(
                file_path=file_path,
                source=extra_params.get("source", "auto"),
                target=extra_params.get("target"),
                output_type=extra_params.get("output_type", "mono"),
                password=password,
                original_name=original_name
            ),
            "PDF翻译"
        )

        report_msg = generate_result_report(results)

    # 根据操作类型选择不同的处理逻辑
    elif operation_config.get("is_edit_operation"):
        # 编辑操作
        edit_type = operation_config.get("edit_type", "")

        # 获取操作描述
        edit_map = {
            "decrypt": "解密", 
            "add_text_watermark": "添加文本水印", 
            "add_image_watermark": "添加图片水印", 
            "encrypt": "加密", 
            "compress": "压缩", 
            "split": "拆分", 
            "merge": "合并", 
            "rotate": "旋转",
            "remove_margin": "去除白边"
        }
        operation_desc = f"PDF{edit_map.get(edit_type, edit_type)}"

        # 处理文件
        results = await process_batch_files(
            file_objects, 
            logger,
            lambda file_path, password, original_name: process_edit_file(
                file_path, edit_type, editor, extra_params, password, original_name
            ),
            operation_desc
        )

        # 生成报告
        report_msg = generate_result_report(results)

    else:
        # 转换操作
        converter = Converter(logger, file_handler)
        format = operation_config.get("format", "")

        # 新增：特殊处理PDF转Markdown和TEX（LaTeX）
        if format in ("md", "tex"):
            oss_map = {
                "md": ("oss://pdf2md", "PDF转Markdown"),
                "tex": ("oss://pdf2tex", "PDF转LaTeX")
            }
            oss_url, operation_desc = oss_map[format]

            results = await process_batch_files(
                file_objects,
                logger,
                lambda file_path, password, original_name: editor.edit_pdf(
                    file_path,
                    edit_type=EditType.EDIT,
                    extra_params={"pages": [{"url": oss_url, "oss_file": ""}]},
                    password=password,
                    original_name=original_name
                ),
                operation_desc
            )

            report_msg = generate_result_report(results)

        elif format == "pdf":
            # 只调用一次process_batch_files，在lambda里分流
            async def pdf_convert_dispatcher(file_path, password, original_name):
                ext = file_handler.get_file_extension(file_path)
                ext_map = {
                    ".txt": ("oss://txt2pdf", "TXT转PDF"),
                    ".tex": ("oss://tex2pdf", "LaTeX转PDF")
                }
                if ext in ext_map:
                    oss_url, operation_desc = ext_map[ext]
                    return await editor.edit_pdf(
                        file_path,
                        edit_type=EditType.EDIT,
                        extra_params={"pages": [{"url": oss_url, "oss_file": ""}]},
                        password=password,
                        original_name=original_name
                    )
                else:
                    return await process_conversion_file(
                        file_path, format, converter, extra_params, password, original_name
                    )

            results = await process_batch_files(
                file_objects,
                logger,
                pdf_convert_dispatcher,
                f"转换为 {format} 格式"
            )

            report_msg = generate_result_report(results)

        else:
            # 获取操作描述
            if format == "doc-repair":
                operation_desc = "去除水印"
            elif format == "number-pdf":
                operation_desc = "添加页码"
            elif format == "flatten-pdf":
                operation_desc = "展平PDF"
            else:
                operation_desc = f"转换为 {format} 格式"

            # 处理文件
            results = await process_batch_files(
                file_objects,
                logger,
                lambda file_path, password, original_name: process_conversion_file(
                    file_path, format, converter, extra_params, password, original_name
                ),
                operation_desc
            )

            # 生成报告
            report_msg = generate_result_report(results)

    # 如果全部失败，记录错误
    if not any(r.success for r in results):
        await logger.error(report_msg)

    return types.TextContent(type="text", text=report_msg)

# 创建Server实例
app = Server(
    name="LightPDF_AI_tools",
    instructions="LightPDF Document Processing Tools.",
)

# 定义工具
@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert_document",
            description="Document format conversion tool.\n\nPDF can be converted to: DOCX, XLSX, PPTX, images (including long images), HTML, TXT (text extraction), CSV, MD (Markdown), or TEX (LaTeX).\nOther formats (DOCX, XLSX, PPTX, images, CAD, CAJ, OFD, HTML, TEX (LaTeX), TXT, ODT) can be converted to PDF. For HTML to PDF, both local HTML files and any web page URL are supported.\n\nPDF to PDF conversion is not supported.\nOnly entire files can be converted.\nFor content-based PDF creation, please use the create_pdf tool. This tool is strictly for file format conversion only.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "File URL, must include protocol, supports http/https/oss."
                                },
                                "password": {
                                    "type": "string",
                                    "description": "Document password, required if the document is password-protected."
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document."
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of files to convert, each containing path and optional password."
                    },
                    "format": {
                        "type": "string",
                        "description": "Target format. PDF can be converted to: DOCX, XLSX, PPTX, images (including long images), HTML, TXT (text extraction), CSV, MD (Markdown), or TEX (LaTeX). Other formats (DOCX, XLSX, PPTX, images, CAD, CAJ, OFD, HTML, TEX (LaTeX), TXT, ODT) can be converted to PDF. For HTML to PDF, both local HTML files and any web page URL are supported. PDF to PDF conversion is not supported.",
                        "enum": ["pdf", "docx", "xlsx", "pptx", "jpg", "jpeg", "png", "html", "txt", "csv", "md", "tex"]
                    },
                    "merge_all": {
                        "type": "integer",
                        "enum": [0, 1],
                        "default": 0,
                        "description": "Only effective in the following scenarios (meaning varies by scenario):\n"
                                       "- PDF to Image: 1 = merge all pages into one long image, 0 = output a separate image for each page;\n"
                                       "- Image to PDF: 1 = merge all images into a single PDF file, 0 = create one PDF file per image;\n"
                                       "- PDF to Excel: 1 = merge all pages into one sheet, 0 = each page is converted into a separate sheet.\n"
                                       "This parameter is ignored for other conversion types."
                    },
                    "one_page_per_sheet": {
                        "type": "boolean",
                        "default": False,
                        "description": "Only effective when converting Excel to PDF. If true, each sheet will be forced to fit into a single PDF page (even if content overflows; no additional pages will be created). If false, each sheet may be split into multiple PDF pages if the content is too large."
                    }
                },
                "required": ["files", "format"]
            }
        ),
        types.Tool(
            name="add_page_numbers",
            description="Add page numbers to each page of a PDF document.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to add page numbers to, each containing path and optional password"
                    },
                    "start_num": {
                        "type": "integer",
                        "description": "Starting page number",
                        "default": 1,
                        "minimum": 1
                    },
                    "position": {
                        "type": "string",
                        "description": "Page number position: 1(top-left), 2(top-center), 3(top-right), 4(bottom-left), 5(bottom-center), 6(bottom-right)",
                        "enum": ["1", "2", "3", "4", "5", "6"],
                        "default": "5"
                    },
                    "margin": {
                        "type": "integer",
                        "description": "Page number margin",
                        "enum": [10, 30, 60],
                        "default": 30
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="remove_watermark",
            description="Remove watermarks from PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to remove watermarks from, each containing path and optional password"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="add_text_watermark",
            description="Add text watermarks to PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to add text watermark to, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to add text watermarks to, each containing path and optional password"
                    },
                    "text": {
                        "type": "string",
                        "description": "Watermark text content"
                    },
                    "position": {
                        "type": "string",
                        "description": "Text watermark position: top-left(topleft), top-center(top), top-right(topright), left(left), center(center), right(right), bottom-left(bottomleft), bottom(bottom), bottom-right(bottomright), diagonal(diagonal, -45 degrees), reverse-diagonal(reverse-diagonal, 45 degrees)",
                        "enum": ["topleft", "top", "topright", "left", "center", "right", 
                                "bottomleft", "bottom", "bottomright", "diagonal", "reverse-diagonal"],
                        "default": "center"
                    },
                    "opacity": {
                        "type": "number",
                        "description": "Opacity, 0.0-1.0",
                        "default": 1.0,
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "range": {
                        "type": "string",
                        "description": "Page range, e.g. '1,3,5-7' or '' (empty string or not set) for all pages"
                    },
                    "layout": {
                        "type": "string",
                        "description": "Layout position: on top of content(on) or under content(under)",
                        "enum": ["on", "under"],
                        "default": "on"
                    },
                    "font_family": {
                        "type": "string",
                        "description": "Font family"
                    },
                    "font_size": {
                        "type": "integer",
                        "description": "Font size"
                    },
                    "font_color": {
                        "type": "string",
                        "description": "Font color, e.g. '#ff0000' for red"
                    }
                },
                "required": ["files", "text", "position"]
            }
        ),
        types.Tool(
            name="add_image_watermark",
            description="Add image watermarks to PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to add image watermark to, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to add image watermarks to, each containing path and optional password"
                    },
                    "image_url": {
                        "type": "string",
                        "description": "Image URL for the watermark, must include protocol, supports http/https/oss"
                    },
                    "position": {
                        "type": "string",
                        "description": "Image watermark position: top-left(topleft), top-center(top), top-right(topright), left(left), center(center), right(right), bottom-left(bottomleft), bottom(bottom), bottom-right(bottomright), diagonal(diagonal, -45 degrees), reverse-diagonal(reverse-diagonal, 45 degrees)",
                        "enum": ["topleft", "top", "topright", "left", "center", "right", 
                                "bottomleft", "bottom", "bottomright", "diagonal", "reverse-diagonal"],
                        "default": "center"
                    },
                    "opacity": {
                        "type": "number",
                        "description": "Opacity, 0.0-1.0",
                        "default": 0.7,
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "range": {
                        "type": "string",
                        "description": "Page range, e.g. '1,3,5-7' or '' (empty string or not set) for all pages"
                    },
                    "layout": {
                        "type": "string",
                        "description": "Layout position: on top of content(on) or under content(under)",
                        "enum": ["on", "under"],
                        "default": "on"
                    }
                },
                "required": ["files", "image_url", "position"]
            }
        ),
        types.Tool(
            name="unlock_pdf",
            description="Remove password protection from PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to decrypt, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required to unlock the document if it is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path", "password"]
                        },
                        "description": "List of PDF files to decrypt, each containing path and password"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="protect_pdf",
            description="Add password protection to PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to encrypt, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to encrypt, each containing path and optional current password"
                    },
                    "password": {
                        "type": "string",
                        "description": "New password to set"
                    }
                },
                "required": ["files", "password"]
            }
        ),
        types.Tool(
            name="compress_pdf",
            description="Reduce the size of PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to compress, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to compress, each containing path and optional password"
                    },
                    "image_quantity": {
                        "type": "integer",
                        "description": "Image quality, 1-100, lower values result in higher compression",
                        "default": 60,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="split_pdf",
            description="Split PDF documents by pages. You can split each page into a separate PDF file, split by specified page ranges, or split by bookmarks/outlines/table of contents/headings (bookmark). Split files can be multiple independent PDF files (returned as a zip package) or merged into a single PDF file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to split, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to split, each containing path and optional password"
                    },
                    "split_type": {
                        "type": "string",
                        "description": "Split type: 'every' (split each page into a separate file), 'page' (split by page ranges), or 'bookmark' (split by PDF bookmarks/outlines/table of contents/headings, each node as a separate PDF file).",
                        "enum": ["every", "page", "bookmark"]
                    },
                    "pages": {
                        "type": "string",
                        "description": "Page ranges to split, e.g. '1,3,5-7' or '' (empty for all pages). Required and only valid when split_type is 'page'."
                    },
                    "merge_all": {
                        "type": "integer",
                        "description": "Whether to merge results into a single PDF file: 1=yes, 0=no (will return a zip package of multiple files). Only valid when split_type is 'page'.",
                        "enum": [0, 1],
                        "default": 0
                    }
                },
                "required": ["files", "split_type"]
            }
        ),
        types.Tool(
            name="merge_pdfs",
            description="Merge multiple PDF files into a single PDF file. You must provide at least two files in the 'files' array, otherwise the operation will fail.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to merge, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to merge (must be at least two), each containing path and optional password"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="rotate_pdf",
            description="Rotate pages in PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to rotate, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to rotate, each containing path and optional password"
                    },
                    "rotates": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "angle": {
                                    "type": "integer",
                                    "description": "Rotation angle, options are 90, 180, 270",
                                    "enum": [90, 180, 270],
                                    "default": 90
                                },
                                "pages": {
                                    "type": "string",
                                    "description": "Specify page ranges to rotate, e.g. '1,3,5-7' or 'all' for all pages",
                                    "default": "all"
                                }
                            },
                            "required": ["angle", "pages"]
                        },
                        "description": "Parameter list, each containing rotation angle and page range"
                    }
                },
                "required": ["files", "rotates"]
            }
        ),
        types.Tool(
            name="remove_margin",
            description="Remove white margins from PDF files (crop page margins).",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to remove margins from, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to remove margins from, each containing path and optional password"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="extract_images",
            description="Extract image resources from all pages of a PDF, supporting multiple image formats.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to extract images from, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to extract images from, each containing path and optional password"
                    },
                    "format": {
                        "type": "string",
                        "description": "Extracted image format",
                        "enum": ["bmp", "png", "gif", "tif", "jpg"],
                        "default": "png"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="flatten_pdf",
            description="Flatten PDF files (convert editable elements such as text, form fields, annotations, and layers into non-editable static content or fixed content).",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to flatten, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to flatten, each containing path and optional password"
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="restrict_printing",
            description="Restrict PDF printing permission. This tool will set a permission password to the PDF so that printing is not allowed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to restrict printing, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to restrict printing, each containing path and optional password"
                    },
                    "password": {
                        "type": "string",
                        "description": "New permission password to set"
                    }
                },
                "required": ["files", "password"]
            }
        ),
        types.Tool(
            name="translate_pdf",
            description="Translate only the text in a PDF file into a specified target language and output a new PDF file. All non-text elements (such as images, tables, and layout) will remain unchanged.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL, must include protocol, supports http/https/oss."
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected."
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document."
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to translate, each containing path and optional password."
                    },
                    "source": {
                        "type": "string",
                        "description": "Source language. Supports 'auto' for automatic detection.",
                        "enum": ["auto", "ar", "bg", "cz", "da", "de", "el", "en", "es", "fi", "fr", "hbs", "hi", "hu", "id", "it", "ja", "ko", "ms", "nl", "no", "pl", "pt", "ru", "sl", "sv", "th", "tr", "vi", "zh", "zh-tw"],
                        "default": "auto"
                    },
                    "target": {
                        "type": "string",
                        "description": "Target language. Must be specified. ar: Arabic, bg: Bulgarian, cz: Czech, da: Danish, de: German, el: Greek, en: English, es: Spanish, fi: Finnish, fr: French, hbs: Croatian, hi: Hindi, hu: Hungarian, id: Indonesian, it: Italian, ja: Japanese, ko: Korean, ms: Malay, nl: Dutch, no: Norwegian, pl: Polish, pt: Portuguese, ru: Russian, sl: Slovenian, sv: Swedish, th: Thai, tr: Turkish, vi: Vietnamese, zh: Simplified Chinese, zh-tw: Traditional Chinese.",
                        "enum": ["ar", "bg", "cz", "da", "de", "el", "en", "es", "fi", "fr", "hbs", "hi", "hu", "id", "it", "ja", "ko", "ms", "nl", "no", "pl", "pt", "ru", "sl", "sv", "th", "tr", "vi", "zh", "zh-tw"]
                    },
                    "output_type": {
                        "type": "string",
                        "description": "Output type: 'mono' for target language only, 'dual' for source/target bilingual output.",
                        "enum": ["mono", "dual"],
                        "default": "mono"
                    }
                },
                "required": ["files", "target"]
            }
        ),
        types.Tool(
            name="resize_pdf",
            description="Resize PDF pages. You can specify the target page size (a0/a1/a2/a3/a4/a5/a6/letter) and/or the image resolution (dpi, e.g., 72). If not set, the corresponding property will not be changed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "PDF file URL to resize, must include protocol, supports http/https/oss"
                                },
                                "password": {
                                    "type": "string",
                                    "description": "PDF document password, required if the document is password-protected"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Original filename of the document"
                                }
                            },
                            "required": ["path"]
                        },
                        "description": "List of PDF files to resize, each containing path and optional password"
                    },
                    "page_size": {
                        "type": "string",
                        "description": "Target page size. Any valid page size name is supported (e.g., a4, letter, legal, etc.), or use width,height in points (pt, e.g., 595,842). If not set, page size will not be changed."
                    },
                    "resolution": {
                        "type": "integer",
                        "description": "Image resolution (dpi), e.g., 72. If not set, resolution will not be changed."
                    }
                },
                "required": ["files"]
            }
        ),
        types.Tool(
            name="create_pdf",
            description="Create a PDF file from LaTeX source code string only. File upload is NOT supported. If you want to convert a TEX file to PDF, please use the convert_document tool instead. This tool only accepts pure LaTeX code as input.",
            inputSchema={
                "type": "object",
                "properties": {
                    "latex_code": {
                        "type": "string",
                        "description": "The LaTeX source code string to be compiled into a PDF file. Only pure LaTeX code as a string is allowed; file upload, file path, or file content is NOT supported. If you have a TEX file, use the convert_document tool."
                    },
                    "filename": {
                        "type": "string",
                        "description": "The filename for the generated PDF"
                    }
                },
                "required": ["latex_code", "filename"]
            }
        ),
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    # 创建日志记录器
    logger = Logger(app.request_context)
    
    # 定义工具配置和默认参数值
    TOOL_CONFIG = {
        "convert_document": {
            "format_key": "format",  # 从arguments获取format
            "is_edit_operation": False,
            "param_keys": ["merge_all", "one_page_per_sheet"]
        },
        "remove_watermark": {
            "format": "doc-repair",  # 固定format
            "is_edit_operation": False,
        },
        "add_page_numbers": {
            "format": "number-pdf",  # 固定format
            "is_edit_operation": False,
            "param_keys": ["start_num", "position", "margin"]  # 需要从arguments获取的参数
        },
        "flatten_pdf": {
            "format": "flatten-pdf",  # 固定format
            "is_edit_operation": False
        },
        "resize_pdf": {
            "format": "resize-pdf",
            "is_edit_operation": False,
            "param_keys": ["page_size", "resolution"]
        },
        "unlock_pdf": {
            "edit_type": "decrypt",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
        },
        "add_text_watermark": {
            "edit_type": "add_text_watermark",  # 编辑类型，文本水印
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["text", "position", "opacity", "range", "layout", 
                          "font_family", "font_size", "font_color"]  # 需要从arguments获取的参数（文本水印）
        },
        "add_image_watermark": {
            "edit_type": "add_image_watermark",
            "is_edit_operation": True,
            "param_keys": ["image_url", "position", "opacity", "range", "layout"]
        },
        "protect_pdf": {
            "edit_type": "encrypt",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["password"]  # 需要从arguments获取的参数
        },
        "restrict_printing": {
            "edit_type": "encrypt",  # 或protect，和protect_pdf一致
            "is_edit_operation": True,
            "param_keys": ["password"]  # 增加password参数
        },
        "compress_pdf": {
            "edit_type": "compress",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["image_quantity"]  # 需要从arguments获取的参数
        },
        "split_pdf": {
            "edit_type": "split",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["pages", "split_type", "merge_all"]  # 需要从arguments获取的参数
        },
        "merge_pdfs": {
            "edit_type": "merge",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
        },
        "rotate_pdf": {
            "edit_type": "rotate",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["rotates"]  # 只需要rotates参数，移除对旧格式的支持
        },
        "remove_margin": {
            "edit_type": "remove_margin",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
        },
        "extract_images": {
            "edit_type": "extract_image",  # 编辑类型
            "is_edit_operation": True,  # 标记为编辑操作
            "param_keys": ["format"]  # 需要从arguments获取的参数
        },
        "translate_pdf": {
            "is_translate_operation": True,
            "param_keys": ["source", "target", "output_type"]
        },
    }
    
    DEFAULTS = {
        "start_num": 1,
        "position_page_numbers": "5",  # 添加页码的位置默认值
        "position_watermark": "center",  # 水印的位置默认值
        "margin": 30,
        "opacity": 1.0,
        "range": "",
        "layout": "on",  # 添加layout默认值
        "image_quantity": 60,
        "split_type": "page",
        "merge_all": 0,
        "angle": 90,
        "pages": "",
        "format": "png",  # 提取图片的默认格式
        "page_size": "",
        "resolution": 0,
    }
    
    if name in TOOL_CONFIG:
        # 处理文件信息
        file_objects = arguments.get("files", [])
        if not file_objects:
            error_msg = "未提供文件信息"
            await logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
        
        # 确保file_objects是一个列表
        if isinstance(file_objects, dict):
            file_objects = [file_objects]
            
        config = TOOL_CONFIG[name]
        operation_config = dict(config)  # 复制配置
        
        # 处理格式
        if not operation_config.get("format") and "format_key" in config:
            operation_config["format"] = arguments.get(config["format_key"], "")
        
        # 处理额外参数
        if "param_keys" in config:
            operation_config["extra_params"] = {}
            
            # 处理特殊情况：position参数在不同工具中有不同的默认值
            for key in config["param_keys"]:
                if key == "position":
                    if name == "add_page_numbers":
                        # 添加页码工具使用"5"作为position默认值
                        operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get("position_page_numbers"))
                    elif name == "add_text_watermark":
                        # 添加文本水印工具使用"center"作为position默认值
                        operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get("position_watermark"))
                    else:
                        # 其他工具使用通用默认值
                        operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get(key))
                else:
                    # 其他参数正常处理
                    operation_config["extra_params"][key] = arguments.get(key, DEFAULTS.get(key, ""))
            
            # restrict_printing工具自动加provider参数
            if name == "restrict_printing":
                operation_config["extra_params"]["provider"] = "printpermission"
        
        # 特殊处理merge_pdfs工具
        if name == "merge_pdfs":
            # 创建编辑器
            file_handler = FileHandler(logger)
            editor = Editor(logger, file_handler)
            
            # 提取文件路径、密码和原始名称
            file_paths = [file_obj["path"] for file_obj in file_objects]
            passwords = [file_obj.get("password") for file_obj in file_objects]
            original_names = [file_obj.get("name") for file_obj in file_objects]
            
            # 由于merge_pdfs方法只接受一个密码参数，如果文件密码不同，可能需要特殊处理
            # 此处简化处理，使用第一个非空密码
            password = next((p for p in passwords if p), None)
            
            # 合并文件名用于结果文件
            merged_name = None
            if any(original_names):
                # 如果有原始文件名，则合并它们（最多使用前两个文件名）
                valid_names = [name for name in original_names if name]
                if valid_names:
                    if len(valid_names) == 1:
                        merged_name = valid_names[0]
                    else:
                        merged_name = f"{valid_names[0]}_{valid_names[1]}_等"
            
            # 直接调用merge_pdfs方法
            result = await editor.merge_pdfs(file_paths, password, merged_name)
            
            # 构建结果报告
            report_msg = generate_result_report(
                [result]
            )
            
            # 如果失败，记录错误
            if not result.success:
                await logger.error(report_msg)
            
            return [types.TextContent(type="text", text=report_msg)]
        
        # 调用通用处理函数
        result = await process_tool_call(logger, file_objects, operation_config)
        return [result]

    elif name == "create_pdf":
        from .create_pdf import create_pdf_from_latex
        latex_code = arguments.get("latex_code")
        filename = arguments.get("filename")
        if not latex_code:
            error_msg = "latex_code参数不能为空"
            await logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
        if not filename:
            error_msg = "filename参数不能为空"
            await logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]

        result = await create_pdf_from_latex(latex_code, logger=logger, original_name=filename)
        # 构建结果报告
        report_msg = generate_result_report(
            [result]
        )
        # 如果失败，记录错误
        if not result.success:
            await logger.error(report_msg)
        
        return [types.TextContent(type="text", text=report_msg)]

    else:
        error_msg = f"未知工具: {name}"
        await logger.error(error_msg, ValueError)
        return [types.TextContent(type="text", text=error_msg)]

async def main():
    """应用主入口"""
    # 打印版本号
    try:
        import importlib.metadata
        version = importlib.metadata.version("lightpdf-aipdf-mcp")
        print(f"LightPDF AI-PDF MCP Server v{version}", file=sys.stderr)
    except Exception as e:
        print("LightPDF AI-PDF MCP Server (版本信息获取失败)", file=sys.stderr)
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="LightPDF AI-PDF MCP Server")
    parser.add_argument("-p", "--port", type=int, default=0, help="指定SSE服务器的端口号，如果提供则使用SSE模式，否则使用stdio模式")
    args = parser.parse_args()
    
    initialization_options = app.create_initialization_options(
        notification_options=NotificationOptions()
    )
    
    if args.port:
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        import uvicorn
            
        # 使用SSE服务器
        print(f"启动SSE服务器，端口号：{args.port}", file=sys.stderr)
        
        # 创建SSE传输
        transport = SseServerTransport("/messages/")
        
        # 定义SSE连接处理函数
        async def handle_sse(request):
            async with transport.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], initialization_options
                )
        
        # 创建Starlette应用
        sse_app = Starlette(routes=[
            Route("/sse/", endpoint=handle_sse),
            Mount("/messages/", app=transport.handle_post_message),
        ])
        
        # 使用异步方式启动服务器
        server = uvicorn.Server(uvicorn.Config(
            app=sse_app,
            host="0.0.0.0",
            port=args.port,
            log_level="warning"
        ))
        await server.serve()
    else:
        import mcp.server.stdio as stdio

        # 使用stdio服务器
        print("启动stdio服务器", file=sys.stderr)
        async with stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                initialization_options
            )

def cli_main():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器被用户中断", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"服务器发生错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli_main()