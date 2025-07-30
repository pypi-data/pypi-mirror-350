"""
Orion Browser: 浏览器代理服务器包

该包提供了浏览器代理功能，可以用作独立服务或导入为Python包使用。
"""

# 直接从app模块导入BrowserManager
from app.tools.browser.browser_manager import BrowserManager
from app.types.messages import BrowserActionRequest
from app.types.browser_types import (
    BrowserAction, GoToUrlAction, NoParamAction, ScrollToTextAction,
    GetDropdownOptionsAction, SelectDropdownOptionAction, ViewAction,
    DoneAction, SaveImageAction, SaveScreenshotAction, ExtractPageContentAction,
    BrowserNavigateAction, BrowserViewAction, BrowserScreenshotAction,
    BrowserRestartAction, BrowserClickAction, BrowserMoveMouseAction,
    BrowserInputAction, BrowserPressKeyAction, BrowserScrollUpAction,
    BrowserScrollDownAction, BrowserSelectOptionAction, BrowserConsoleExecAction,
    BrowserConsoleViewAction, SearchBaiduAction, ClickElementAction, InputTextAction,
    ClickByPositionAction,OpenTabAction, ScrollAction, SwitchTabAction, SendKeysAction, BrowserActionResult,
    GetAllTabsAction
)

# 导出核心组件和所有 action 类型
__all__ = [
    "BrowserManager", 
    "BrowserActionRequest",
    "BrowserAction", 
    "GoToUrlAction",
    "NoParamAction",
    "ScrollToTextAction",
    "GetDropdownOptionsAction", 
    "SelectDropdownOptionAction", 
    "ViewAction",
    "DoneAction", 
    "SaveImageAction", 
    "SaveScreenshotAction", 
    "ExtractPageContentAction",
    "BrowserNavigateAction", 
    "BrowserViewAction", 
    "BrowserScreenshotAction",
    "BrowserRestartAction", 
    "BrowserClickAction", 
    "BrowserMoveMouseAction",
    "BrowserInputAction", 
    "BrowserPressKeyAction", 
    "BrowserScrollUpAction",
    "BrowserScrollDownAction", 
    "BrowserSelectOptionAction", 
    "BrowserConsoleExecAction",
    "BrowserConsoleViewAction", 
    "SearchBaiduAction", 
    "ClickElementAction", 
    "ClickByPositionAction",
    "InputTextAction",
    "OpenTabAction", 
    "GetAllTabsAction",
    "ScrollAction", 
    "SwitchTabAction", 
    "SendKeysAction",
    "BrowserActionResult"
] 