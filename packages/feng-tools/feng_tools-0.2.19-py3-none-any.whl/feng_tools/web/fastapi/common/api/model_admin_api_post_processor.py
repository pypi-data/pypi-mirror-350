from typing import Any

from starlette.requests import Request

from feng_tools.web.fastapi.common.api.model_admin_api import ModelAdminApi


class ModelAdminApiPostProcessor(ModelAdminApi):
    """模型管理API后置处理器"""

    
    def add_api_process(self, request: Request, data:Any, **kwargs):
        """添加接口处理"""
        pass

    
    def read_api_process(self, request: Request, data:Any, **kwargs):
        """查看接口处理"""
        pass

    
    def update_api_process(self, request: Request, data:Any, **kwargs):
        """更新接口处理"""
        pass

    
    def delete_api_process(self, request: Request, data:Any, **kwargs):
        """删除接口处理"""
        pass

    def delete_batch_api_process(self, request: Request, data:Any, **kwargs):
        """批量删除接口处理"""
        pass
    def list_api_process(self, request: Request, data:Any, **kwargs):
        """列表接口处理"""
        pass

    
    def list_by_page_api_process(self, request: Request, data:Any, **kwargs):
        """分页列表接口处理"""
        pass