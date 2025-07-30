# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-04-12 15:55
# @Author : 毛鹏
import os
import traceback

import time
from playwright._impl._errors import TargetClosedError, Error, TimeoutError

from mangotools.assertion import PublicAssertion
from mangotools.decorator import sync_retry
from mangotools.enums import StatusEnum
from ..enums import ElementOperationEnum, DriveTypeEnum
from ..exceptions import MangoAutomationError
from ..exceptions._error_msg import *
from ..models import ElementResultModel, ElementModel
from ..uidrive.android import AndroidDriver
from ..uidrive.web.sync_web import SyncWebDevice, SyncWebAssertion


class SyncElement(SyncWebDevice, AndroidDriver):

    def __init__(self, base_data, element_model: ElementModel, drive_type: int, element_data: dict | None = None):
        super().__init__(base_data)
        self.element_data = element_data
        self.element_model = element_model
        self.drive_type = drive_type
        self.ope_name = element_model.name if element_model.name else element_model.ope_key
        self.element_result_model = ElementResultModel(
            id=self.element_model.id,
            name=self.element_model.name,
            loc=self.element_model.loc,
            exp=self.element_model.exp,
            sub=self.element_model.sub,
            sleep=self.element_model.sleep,

            type=self.element_model.type,
            ope_key=self.element_model.ope_key,
            sql=self.element_model.sql,
            key_list=self.element_model.key_list,
            key=self.element_model.key,
            value=self.element_model.value,

            status=StatusEnum.FAIL.value,
        )

    def open_device(self, is_open: bool = False):
        if self.drive_type == DriveTypeEnum.WEB.value:
            self.open_url(is_open)
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.open_app()
        elif self.drive_type == DriveTypeEnum.DESKTOP.value:
            pass
        else:
            self.base_data.log.error(f'不存在这个类型，如果是非管理员看到这种提示，请联系管理员')
            raise Exception('不存在的设备类型')

    def clean_data(self):
        try:
            for field_name, field_value in self.element_model:
                if field_value is None:
                    continue
                if field_name == "ope_value":
                    for method_model in field_value:
                        for method_field, method_val in method_model:
                            if isinstance(method_val, str):
                                setattr(method_model, method_field, self.base_data.test_data.replace(method_val))
                elif isinstance(field_value, str):
                    setattr(self.element_model, field_name, self.base_data.test_data.replace(field_value))
        except MangoAutomationError as error:
            self.base_data.log.debug(f'操作元素解析数据失败，类型：{type(error)}, 详情：{error}')
            raise MangoAutomationError(error.code, error.msg)

    def element_main(self) -> ElementResultModel:
        try:
            self.__main()
            if self.element_model.sleep:
                time.sleep(self.element_model.sleep)
            self.element_result_model.status = StatusEnum.SUCCESS.value
            self.element_result_model.error_message = None
        except TargetClosedError as error:
            self.base_data.setup()
            self.base_data.log.debug(
                f'浏览器关闭异常，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
            self.element_result_model.status = StatusEnum.FAIL.value
            self.element_result_model.error_message = '浏览器被关闭，请不要认关闭浏览器，非认为管理请联系管理员解决！'
        except MangoAutomationError as error:
            self.__error(error.msg)
            self.base_data.log.debug(f'已知异常，类型：{type(error)}，失败详情：{error}')
        except Error as error:
            self.__error(f'未知错误失败，请检查测试数据，如果需要明确的提示请联系管理员，提示：{error.message}')
            self.base_data.log.error(
                f'未知错误捕获-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
        except Exception as error:
            error_msg = f'未知错误失败，请检查测试数据，如果需要明确的提示请联系管理员，提示：{error.args}'
            if hasattr(error, 'msg'):
                error_msg = error.msg
            self.__error(error_msg)
            self.base_data.log.error(
                f'未知错误捕获-2，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
        return self.element_result_model

    @sync_retry()
    def __main(self):
        self.clean_data()
        if self.element_model.type == ElementOperationEnum.OPE.value:
            self.__ope()
        elif self.element_model.type == ElementOperationEnum.ASS.value:
            self.__ass()
        elif self.element_model.type == ElementOperationEnum.SQL.value:
            self.__sql()
        elif self.element_model.type == ElementOperationEnum.CUSTOM.value:
            self.__custom()
        else:
            raise MangoAutomationError(*ERROR_MSG_0015)

    def __ope(self):
        method_name = getattr(self.element_model, 'ope_key', None)
        if not method_name:
            self.base_data.log.debug('操作失败-1，ope_key 不存在或为空')
            raise MangoAutomationError(*ERROR_MSG_0048)
        if not hasattr(self, method_name):
            self.base_data.log.debug(f'操作失败-2，方法不存在: {method_name}')
            raise MangoAutomationError(*ERROR_MSG_0048)
        if not callable(getattr(self, method_name)):
            self.base_data.log.debug(f'操作失败-3，属性不可调用: {method_name}')
            raise MangoAutomationError(*ERROR_MSG_0048)
        if self.element_model.ope_value is None:
            raise MangoAutomationError(*ERROR_MSG_0054)

        self.__ope_value()
        if self.drive_type == DriveTypeEnum.WEB.value:
            self.web_action_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_action_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        else:
            pass
        for i in self.element_model.ope_value:
            if i.d:
                self.element_result_model.ope_value[i.f] = i.v

    def __ass(self):
        if self.element_model.ope_value is None:
            raise MangoAutomationError(*ERROR_MSG_0053)
        self.__ope_value(True)
        if self.drive_type == DriveTypeEnum.WEB.value:
            self.web_assertion_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_assertion_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        else:
            pass
        for i in self.element_model.ope_value:
            if i.d:
                self.element_result_model.ope_value[i.f] = i.v

    def __sql(self):
        if not self.element_data:
            sql = self.base_data.test_data.replace(self.element_model.sql)
            key_list = self.element_model.key_list
        else:
            sql = self.base_data.test_data.replace(self.element_data.get('sql'))
            key_list = self.element_data.get('key_list')
        if self.base_data.mysql_connect:
            result_list: list[dict] = self.base_data.mysql_connect.condition_execute(sql)
            if isinstance(result_list, list):
                for result in result_list:
                    try:
                        for value, key in zip(result, key_list):
                            self.base_data.test_data.set_cache(key, result.get(value))
                    except SyntaxError as error:
                        self.base_data.log.debug(
                            f'SQL执行失败-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
                        raise MangoAutomationError(*ERROR_MSG_0038)

                if not result_list:
                    raise MangoAutomationError(*ERROR_MSG_0036, value=(self.element_model.sql,))

    def __custom(self):
        if not self.element_data:
            key = self.element_model.key
            value = self.element_model.value
        else:
            key = self.element_data.get('key')
            value = self.element_data.get('value')
        self.base_data.test_data.set_cache(key, self.base_data.test_data.replace(value))

    def __ope_value(self, is_ass: bool = False):
        try:
            ope_key = 'actual' if is_ass else 'locating'
            for i in self.element_model.ope_value:
                if i.f == ope_key and self.element_model.loc:
                    find_params = {
                        'name': self.element_model.name,
                        '_type': self.element_model.type,
                        'exp': self.element_model.exp,
                        'loc': self.element_model.loc,
                        'sub': self.element_model.sub
                    }
                    if self.drive_type == DriveTypeEnum.WEB.value:
                        loc, \
                            self.element_result_model.ele_quantity, \
                            self.element_result_model.element_text \
                            = self.web_find_ele(**find_params, is_iframe=self.element_model.is_iframe)
                    elif self.drive_type == DriveTypeEnum.ANDROID.value:
                        loc, \
                            self.element_result_model.ele_quantity, \
                            self.element_result_model.element_text \
                            = self.a_find_ele(**find_params)
                    else:
                        loc, \
                            self.element_result_model.ele_quantity, \
                            self.element_result_model.element_text \
                            = None, 0, None

                    if is_ass:
                        if callable(getattr(SyncWebAssertion, self.element_model.ope_key, None)):
                            i.v = loc
                        elif callable(getattr(PublicAssertion, self.element_model.ope_key, None)):
                            i.v = self.element_result_model.element_text
                    else:
                        i.v = loc
                else:
                    if self.element_data:
                        for ele_name, case_data in self.element_data.items():
                            if ele_name == i.f:
                                value = case_data
                                i.v = self.base_data.test_data.replace(value)

        except AttributeError as error:
            self.base_data.log.debug(
                f'获取操作值失败-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
            raise MangoAutomationError(*ERROR_MSG_0027)

    def __error(self, msg: str):
        self.element_result_model.status = StatusEnum.FAIL.value
        self.element_result_model.error_message = msg
        self.base_data.log.debug(
            f"""
            元素操作失败----->
            元 素 对 象：{self.element_model.model_dump() if self.element_model else self.element_model}
            元素测试结果：{
            self.element_result_model.model_dump() if self.element_result_model else self.element_result_model}
            """
        )
        file_name = f'失败截图-{self.element_model.name}{self.base_data.test_data.get_time_for_min()}.jpg'
        file_path = os.path.join(self.base_data.screenshot_path, file_name)
        self.element_result_model.picture_path = file_path
        self.element_result_model.picture_name = file_name
        self.__error_screenshot(file_path)

    def __error_screenshot(self, file_path):
        if self.drive_type == DriveTypeEnum.WEB.value:
            try:
                self.w_screenshot(file_path)
            except (TargetClosedError, TimeoutError) as error:
                self.base_data.log.debug(
                    f'截图出现异常失败-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
                self.base_data.setup()
                raise MangoAutomationError(*ERROR_MSG_0010)
            except AttributeError as error:
                self.base_data.log.debug(
                    f'截图出现异常失败-2，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
                self.base_data.setup()
                raise MangoAutomationError(*ERROR_MSG_0010)
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_screenshot(file_path)
        else:
            pass
