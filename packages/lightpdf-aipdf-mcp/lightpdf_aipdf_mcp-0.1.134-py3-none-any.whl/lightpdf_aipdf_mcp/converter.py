"""PDF文档转换模块"""
import os
import httpx

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set

from .common import BaseResult, Logger, FileHandler, BaseApiClient

class InputFormat(str, Enum):
    """支持的输入文件格式"""
    PDF = "pdf"
    WORD = "docx"
    EXCEL = "xlsx"
    PPT = "pptx"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    CAD = "dwg"
    CAJ = "caj"
    OFD = "ofd"
    HTML = "html"

class OutputFormat(str, Enum):
    """支持的输出文件格式"""
    PDF = "pdf"
    WORD = "docx"
    EXCEL = "xlsx"
    PPT = "pptx"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    HTML = "html"
    TEXT = "txt"
    CSV = "csv"

# 文件扩展名到输入格式的映射
INPUT_EXTENSIONS = {
    ".pdf": InputFormat.PDF,
    ".docx": InputFormat.WORD,
    ".xlsx": InputFormat.EXCEL,
    ".pptx": InputFormat.PPT,
    ".jpg": InputFormat.JPG,
    ".jpeg": InputFormat.JPEG,
    ".png": InputFormat.PNG,
    ".dwg": InputFormat.CAD,
    ".caj": InputFormat.CAJ,
    ".ofd": InputFormat.OFD,
    ".html": InputFormat.HTML,
}

# 输入格式到可用输出格式的映射
FORMAT_CONVERSION_MAP = {
    InputFormat.PDF: {
        OutputFormat.WORD,   # PDF转Word
        OutputFormat.EXCEL,  # PDF转Excel
        OutputFormat.PPT,    # PDF转PPT
        OutputFormat.JPG,    # PDF转JPG
        OutputFormat.JPEG,   # PDF转JPEG
        OutputFormat.PNG,    # PDF转PNG
        OutputFormat.HTML,   # PDF转HTML
        OutputFormat.TEXT,   # PDF转文本
        OutputFormat.CSV,    # PDF转CSV
    },
    InputFormat.WORD: {OutputFormat.PDF},    # Word转PDF
    InputFormat.EXCEL: {OutputFormat.PDF},   # Excel转PDF
    InputFormat.PPT: {OutputFormat.PDF},     # PPT转PDF
    InputFormat.JPG: {OutputFormat.PDF},     # JPG转PDF
    InputFormat.JPEG: {OutputFormat.PDF},    # JPEG转PDF
    InputFormat.PNG: {OutputFormat.PDF},     # PNG转PDF
    InputFormat.CAD: {OutputFormat.PDF},     # CAD转PDF
    InputFormat.CAJ: {OutputFormat.PDF},     # CAJ转PDF
    InputFormat.OFD: {OutputFormat.PDF},     # OFD转PDF
    InputFormat.HTML: {OutputFormat.PDF},    # HTML转PDF
}

# 扩展FileHandler类的方法
def get_input_format(file_path: str) -> Optional[InputFormat]:
    """根据文件路径获取输入格式"""
    ext = FileHandler.get_file_extension(file_path)
    return INPUT_EXTENSIONS.get(ext)

def get_available_output_formats(input_format: InputFormat) -> Set[OutputFormat]:
    """获取指定输入格式支持的输出格式"""
    return FORMAT_CONVERSION_MAP.get(input_format, set())

# 为FileHandler类注入方法
FileHandler.get_input_format = staticmethod(get_input_format)
FileHandler.get_available_output_formats = staticmethod(get_available_output_formats)

@dataclass
class ConversionResult(BaseResult):
    """转换结果数据类"""
    pass

class Converter(BaseApiClient):
    """PDF文档转换器"""
    def __init__(self, logger: Logger, file_handler: FileHandler):
        super().__init__(logger, file_handler)
        api_endpoint = os.getenv("API_ENDPOINT", "techsz.aoscdn.com/api")
        self.api_base_url = f"https://{api_endpoint}/tasks/document/conversion"
        self.api_wkhtmltopdf_url = f"https://{api_endpoint}/tasks/document/wkhtmltopdf"

    async def add_page_numbers(self, file_path: str, start_num: int = 1, position: str = "5", margin: int = 30, password: str = None, original_name: Optional[str] = None) -> ConversionResult:
        """为PDF文档添加页码
        
        Args:
            file_path: 要添加页码的PDF文件路径
            start_num: 起始页码，整数类型，默认为1
            position: 页码显示位置，字符串类型，可选值1-6（左上/上中/右上/左下/下中/右下），默认为5（下中）
            margin: 页码显示的边距，整数类型，可选值10/30/60，默认为30
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            original_name: 原始文件名（可选）
            
        Returns:
            ConversionResult: 转换结果
        """
        # 验证输入文件是否为PDF
        input_format = self.file_handler.get_input_format(file_path)
        if input_format != InputFormat.PDF:
            await self.logger.error(f"添加页码功能仅支持PDF文件，当前文件格式为: {self.file_handler.get_file_extension(file_path)}")
            return ConversionResult(success=False, file_path=file_path, error_message="添加页码功能仅支持PDF文件", original_name=original_name)
        
        # 验证参数
        valid_positions = {"1", "2", "3", "4", "5", "6"}
        valid_margins = {10, 30, 60}
        
        # 验证position参数
        if position not in valid_positions:
            error_msg = f"无效的页码位置值: {position}。有效值为: 1(左上), 2(上中), 3(右上), 4(左下), 5(下中), 6(右下)"
            await self.logger.error(error_msg)
            return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)
        
        # 验证margin参数
        if margin not in valid_margins:
            error_msg = f"无效的页码边距值: {margin}。有效值为: 10, 30, 60"
            await self.logger.error(error_msg)
            return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)
        
        # 验证start_num是否为正整数
        if not isinstance(start_num, int) or start_num < 1:
            error_msg = f"起始页码必须是正整数，当前值为: {start_num}"
            await self.logger.error(error_msg)
            return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)
        
        # 构建API参数
        extra_params = {
            "start_num": start_num,
            "position": position,
            "margin": margin
        }
        
        # 记录操作描述
        await self.logger.log("info", f"正在为PDF添加页码（起始页码: {start_num}, 位置: {position}, 边距: {margin}）...")
        
        # 调用convert_file方法处理API请求
        return await self.convert_file(file_path, "number-pdf", extra_params, password, original_name)
        
    async def convert_file(self, file_path: str, format: str, extra_params: dict = None, password: str = None, original_name: Optional[str] = None) -> ConversionResult:
        """转换单个文件
        
        Args:
            file_path: 要转换的文件路径
            format: 目标格式
            extra_params: 额外的API参数，例如去除水印
            password: 文档密码，如果文档受密码保护，则需要提供（可选）
            original_name: 原始文件名（可选）
            
        Returns:
            ConversionResult: 转换结果
        """
        if not self.api_key:
            await self.logger.error("未找到API_KEY。请在客户端配置API_KEY环境变量。")
            return ConversionResult(success=False, file_path=file_path, error_message="未找到API_KEY", original_name=original_name)

        # 特殊格式：doc-repair用于去除水印，number-pdf用于添加页码，输出均为PDF
        is_special_operation = format in ["doc-repair", "number-pdf", "flatten-pdf", "resize-pdf"]
        actual_output_format = "pdf" if is_special_operation else format

        # 检查是否为URL或OSS路径，如果是则跳过文件格式检查
        is_remote_path = self.file_handler.is_url(file_path) or self.file_handler.is_oss_id(file_path)
        
        if not is_remote_path:
            # 只对本地文件进行格式验证
            
            # 验证输入文件格式
            input_format = self.file_handler.get_input_format(file_path)
            if not input_format and not is_special_operation:
                error_msg = f"不支持的输入文件格式: {self.file_handler.get_file_extension(file_path)}"
                await self.logger.error(error_msg)
                return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)

            # 如果是去除水印操作，检查是否PDF文件
            if format == "doc-repair" and input_format != InputFormat.PDF:
                error_msg = "去除水印功能仅支持PDF文件"
                await self.logger.error(error_msg)
                return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)
                
            # 如果是添加页码操作，检查是否PDF文件
            if format == "number-pdf" and input_format != InputFormat.PDF:
                error_msg = "添加页码功能仅支持PDF文件"
                await self.logger.error(error_msg)
                return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)
            
            # 如果是展平PDF操作，检查是否PDF文件
            if format == "flatten-pdf" and input_format != InputFormat.PDF:
                error_msg = "展平PDF功能仅支持PDF文件"
                await self.logger.error(error_msg)
                return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)

            # 如果是调整PDF大小操作，检查是否PDF文件
            if format == "resize-pdf" and input_format != InputFormat.PDF:
                error_msg = "调整PDF大小功能仅支持PDF文件"
                await self.logger.error(error_msg)
                return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)

            # 验证输出格式（除去特殊操作外）
            if not is_special_operation:
                try:
                    output_format = OutputFormat(format)
                except ValueError:
                    error_msg = f"不支持的输出格式: {format}"
                    await self.logger.error(error_msg)
                    return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)

        else:
            # 远程路径的情况，设置必要的变量以便后续使用
            if not is_special_operation:
                try:
                    output_format = OutputFormat(format)
                except ValueError:
                    error_msg = f"不支持的输出格式: {format}"
                    await self.logger.error(error_msg)
                    return ConversionResult(success=False, file_path=file_path, error_message=error_msg, original_name=original_name)
            else:
                output_format = OutputFormat.PDF
            
            # 对于远程路径，无法确定输入格式，但为了让后续代码能正常运行，设置一个默认值
            input_format = None

        # 验证文件
        exists = await self.file_handler.validate_file_exists(file_path)
        if not exists:
            return ConversionResult(success=False, file_path=file_path, error_message="文件不存在", original_name=original_name)

        # 操作描述
        if format == "doc-repair":
            operation_desc = "去除水印"
        elif format == "number-pdf":
            operation_desc = "添加页码"
        elif format == "flatten-pdf":
            operation_desc = "展平PDF"
        elif format == "resize-pdf":
            operation_desc = "调整PDF大小"
        else:
            if is_remote_path:
                operation_desc = f"转换为 {output_format.value.upper()} 格式"
            else:
                if input_format:
                    operation_desc = f"将 {input_format.value.upper()} 转换为 {output_format.value.upper()} 格式"
                else:
                    operation_desc = f"转换为 {output_format.value.upper()} 格式"
        await self.logger.log("info", f"正在{operation_desc}...")

        import httpx
        async with httpx.AsyncClient(timeout=3600.0) as client:
            task_id = None
            try:
                # 初始化extra_params（如果为None）
                if extra_params is None:
                    extra_params = {}
                
                # 如果提供了密码，将其添加到extra_params
                if password:
                    extra_params["password"] = password

                if original_name:
                    extra_params["filename"] = os.path.splitext(original_name)[0]
                
                one_page_per_sheet = extra_params.pop("one_page_per_sheet", False)
                if one_page_per_sheet:
                    extra_params["provider"] = "apower"

                # 创建转换任务
                task_id = await self._create_task(client, file_path, format, extra_params)
                
                # 等待任务完成
                download_url = await self._wait_for_task(client, task_id, "转换")
                
                # 记录完成信息
                await self.logger.log("info", "转换完成。可通过下载链接获取结果文件。")
                
                return ConversionResult(
                    success=True,
                    file_path=file_path,
                    error_message=None,
                    download_url=download_url,
                    original_name=original_name,
                    task_id=task_id
                )

            except Exception as e:
                return ConversionResult(
                    success=False,
                    file_path=file_path,
                    error_message=str(e),
                    download_url=None,
                    original_name=original_name,
                    task_id=task_id
                )

    async def _create_task(self, client: httpx.AsyncClient, file_path: str, format: str, extra_params: dict = None) -> str:
        """创建转换任务
        
        Args:
            client: HTTP客户端
            file_path: 文件路径
            format: 目标格式，特殊格式"doc-repair"用于去除水印，"number-pdf"用于添加页码
            extra_params: 额外API参数(可选)
        
        Returns:
            str: 任务ID
        """
        await self.logger.log("info", "正在提交转换任务...")
        
        headers = {"X-API-KEY": self.api_key}
        data = {"format": format}
        
        # 添加额外参数
        if extra_params:
            data.update(extra_params)
        
        api_url = self.api_base_url
        # html转pdf特殊接口处理
        if format == "pdf":
            ext = self.file_handler.get_file_extension(file_path)
            # 支持直接转PDF的文件后缀
            direct_pdf_exts = {".docx", ".xlsx", ".pptx", ".jpg", ".jpeg", ".png", ".dwg", ".caj", ".ofd", ".html", ".txt", ".tex", ".odt"}
            # 本地.html 或 URL 且后缀不在direct_pdf_exts都走wkhtmltopdf
            if ext == ".html" or (file_path and file_path.startswith(("http://", "https://")) and ext not in direct_pdf_exts):
                api_url = self.api_wkhtmltopdf_url
        
        # 检查是否为OSS路径
        if self.file_handler.is_oss_id(file_path):
            # OSS路径处理方式，与URL类似，但提取resource_id
            data["resource_id"] = file_path.split("oss_id://")[1]
            # 使用JSON方式时添加Content-Type
            headers["Content-Type"] = "application/json"
            response = await client.post(
                api_url,
                json=data,
                headers=headers
            )
        # 检查是否为URL路径
        elif self.file_handler.is_url(file_path):
            # arxiv.org/pdf/特殊处理
            if isinstance(file_path, str) and "arxiv.org/pdf/" in file_path:
                from urllib.parse import urlparse, urlunparse
                url_obj = urlparse(file_path)
                if not url_obj.path.endswith(".pdf"):
                    new_path = url_obj.path + ".pdf"
                    file_path = urlunparse(url_obj._replace(path=new_path))
            data["url"] = file_path
            # 使用JSON方式时添加Content-Type
            headers["Content-Type"] = "application/json"
            response = await client.post(
                api_url,
                json=data,
                headers=headers
            )
        else:
            # 对于文件上传，使用表单方式，不需要添加Content-Type
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = await client.post(
                    api_url,
                    files=files,
                    data=data,
                    headers=headers
                )
        
        # 使用基类的方法处理API响应
        return await self._handle_api_response(response, "创建任务") 