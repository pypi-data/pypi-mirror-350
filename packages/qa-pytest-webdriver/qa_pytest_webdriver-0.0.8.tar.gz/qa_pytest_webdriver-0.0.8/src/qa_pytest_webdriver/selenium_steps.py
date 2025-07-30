# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from typing import (
    Callable,
    Iterator,
    List,
    Optional,
    Protocol,
    Self,
    Tuple,
    Union,
    final,
    overload,
)
from hamcrest.core.matcher import Matcher

from selenium.webdriver.common.by import By as _By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from qa_pytest_webdriver.selenium_configuration import SeleniumConfiguration
from qa_pytest_commons.generic_steps import GenericSteps
from qa_testing_utils.logger import traced


class SearchContext(Protocol):
    def find_element(self, by: str, value: Optional[str]) -> WebElement: ...

    def find_elements(
        self, by: str, value: Optional[str]) -> List[WebElement]: ...


@dataclass(frozen=True)
class Locator:
    by: str
    value: str

    def as_tuple(self) -> Tuple[str, str]:
        return (self.by, self.value)


class By:

    @staticmethod
    def id(value: str) -> Locator:
        return Locator(_By.ID, value)

    @staticmethod
    def xpath(value: str) -> Locator:
        return Locator(_By.XPATH, value)

    @staticmethod
    def link_text(value: str) -> Locator:
        return Locator(_By.LINK_TEXT, value)

    @staticmethod
    def partial_link_text(value: str) -> Locator:
        return Locator(_By.PARTIAL_LINK_TEXT, value)

    @staticmethod
    def name(value: str) -> Locator:
        return Locator(_By.NAME, value)

    @staticmethod
    def tag_name(value: str) -> Locator:
        return Locator(_By.TAG_NAME, value)

    @staticmethod
    def class_name(value: str) -> Locator:
        return Locator(_By.CLASS_NAME, value)

    @staticmethod
    def css_selector(value: str) -> Locator:
        return Locator(_By.CSS_SELECTOR, value)


ElementSupplier = Callable[[], WebElement]
LocatorOrSupplier = Union[Locator, ElementSupplier]


class SeleniumSteps[TConfiguration: SeleniumConfiguration](
    GenericSteps[TConfiguration]
):
    _web_driver: WebDriver

    @final
    @traced
    def clicking_once(self, element_supplier: ElementSupplier) -> Self:
        element_supplier().click()
        return self

    @overload
    def clicking(self, element: Locator) -> Self: ...

    @overload
    def clicking(self, element: ElementSupplier) -> Self: ...

    @final
    def clicking(self, element: LocatorOrSupplier) -> Self:
        return self.retrying(lambda: self.clicking_once(self._resolve(element)))

    @final
    @traced
    def typing_once(self, element_supplier: ElementSupplier, text: str) -> Self:
        element = element_supplier()
        element.clear()
        element.send_keys(text)
        return self

    @overload
    def typing(self, element: Locator, text: str) -> Self: ...

    @overload
    def typing(self, element: ElementSupplier, text: str) -> Self: ...

    @final
    def typing(self, element: LocatorOrSupplier, text: str) -> Self:
        return self.retrying(lambda: self.typing_once(self._resolve(element), text))

    @final
    def the_element(self, locator: Locator, by_rule: Matcher[WebElement], context: Optional[SearchContext] = None) -> Self:
        return self.eventually_assert_that(lambda: self._element(locator, context), by_rule)

    @final
    def the_elements(self, locator: Locator, by_rule: Matcher[Iterator[WebElement]], context: Optional[SearchContext] = None) -> Self:
        return self.eventually_assert_that(lambda: self._elements(locator, context), by_rule)

    @final
    @traced
    def _elements(
        self, locator: Locator, context: Optional[SearchContext] = None
    ) -> Iterator[WebElement]:
        return iter((context or self._web_driver).find_elements(*locator.as_tuple()))

    @final
    @traced
    def _element(
        self, locator: Locator, context: Optional[SearchContext] = None
    ) -> WebElement:
        return self._scroll_into_view(
            (context or self._web_driver).find_element(*locator.as_tuple())
        )

    def _scroll_into_view(self, element: WebElement) -> WebElement:
        self._web_driver.execute_script( # type: ignore
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return element

    @final
    def _resolve(self, element: LocatorOrSupplier) -> ElementSupplier:
        if isinstance(element, Locator):
            return lambda: self._element(element)
        return element
