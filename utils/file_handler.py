"""
文件处理工具模块
功能：读取和验证不同格式的简历文件
"""
import os
from typing import Dict, Any, Optional
from werkzeug.datastructures import FileStorage


class FileHandler:
    """文件处理器"""

    # 支持的文件类型及其 MIME 类型
    ALLOWED_EXTENSIONS = {
        'txt': ['text/plain'],
        'pdf': ['application/pdf'],
        'docx': [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/octet-stream'  # 有时 docx 会被识别为这个类型
        ],
        'doc': ['application/msword']
    }

    # 最大文件大小 (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    @classmethod
    def validate_file(cls, file: FileStorage) -> Dict[str, Any]:
        """
        验证上传的文件

        Args:
            file: Flask 上传的文件对象

        Returns:
            验证结果字典
        """
        # 检查文件是否存在
        if not file:
            return {
                "success": False,
                "message": "未检测到文件"
            }

        # 检查文件名是否为空
        if file.filename == '':
            return {
                "success": False,
                "message": "文件名不能为空"
            }

        # 获取文件扩展名
        filename = file.filename.lower()
        if '.' not in filename:
            return {
                "success": False,
                "message": "文件必须有扩展名"
            }

        extension = filename.rsplit('.', 1)[1]

        # 检查文件类型
        if extension not in cls.ALLOWED_EXTENSIONS:
            return {
                "success": False,
                "message": f"不支持的文件类型。支持的格式: {', '.join(cls.ALLOWED_EXTENSIONS.keys())}"
            }

        # 检查 MIME 类型
        if file.content_type not in cls.ALLOWED_EXTENSIONS[extension]:
            return {
                "success": False,
                "message": f"文件 MIME 类型不匹配。期望: {cls.ALLOWED_EXTENSIONS[extension]}, 实际: {file.content_type}"
            }

        # 检查文件大小
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # 重置文件指针

        if file_size == 0:
            return {
                "success": False,
                "message": "文件内容为空"
            }

        if file_size > cls.MAX_FILE_SIZE:
            return {
                "success": False,
                "message": f"文件大小超过限制。最大允许: {cls.MAX_FILE_SIZE / 1024 / 1024}MB"
            }

        return {
            "success": True,
            "message": "文件验证通过",
            "data": {
                "filename": file.filename,
                "extension": extension,
                "size": file_size,
                "content_type": file.content_type
            }
        }

    @classmethod
    def extract_text(cls, file: FileStorage) -> Dict[str, Any]:
        """
        从文件中提取文本内容

        Args:
            file: Flask 上传的文件对象

        Returns:
            包含提取文本的结果字典
        """
        # 先验证文件
        validation_result = cls.validate_file(file)
        if not validation_result['success']:
            return validation_result

        extension = validation_result['data']['extension']

        try:
            # 根据文件类型提取文本
            if extension == 'txt':
                text = cls._extract_from_txt(file)
            elif extension == 'pdf':
                text = cls._extract_from_pdf(file)
            elif extension in ['doc', 'docx']:
                text = cls._extract_from_docx(file)
            else:
                return {
                    "success": False,
                    "message": f"不支持的文件类型: {extension}"
                }

            # 检查提取的文本是否为空
            if not text or not text.strip():
                return {
                    "success": False,
                    "message": "未能从文件中提取到文本内容"
                }

            return {
                "success": True,
                "data": {
                    "text": text,
                    "filename": file.filename,
                    "file_info": validation_result['data']
                },
                "message": "文本提取成功"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"文件处理失败: {str(e)}"
            }

    @staticmethod
    def _extract_from_txt(file: FileStorage) -> str:
        """从 TXT 文件提取文本"""
        # 尝试不同的编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']

        content = file.read()
        file.seek(0)  # 重置文件指针

        for encoding in encodings:
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                continue

        # 如果所有编码都失败，使用 utf-8 并忽略错误
        return content.decode('utf-8', errors='ignore')

    @staticmethod
    def _extract_from_pdf(file: FileStorage) -> str:
        """从 PDF 文件提取文本"""
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("请安装 PyPDF2: pip install PyPDF2")

        pdf_reader = PyPDF2.PdfReader(file)
        text_parts = []

        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())

        file.seek(0)  # 重置文件指针
        return '\n'.join(text_parts)

    @staticmethod
    def _extract_from_docx(file: FileStorage) -> str:
        """从 DOCX 文件提取文本"""
        try:
            from docx import Document
        except ImportError:
            raise ImportError("请安装 python-docx: pip install python-docx")

        doc = Document(file)
        text_parts = []

        for paragraph in doc.paragraphs:
            text_parts.append(paragraph.text)

        file.seek(0)  # 重置文件指针
        return '\n'.join(text_parts)
