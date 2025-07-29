import re
from enum import Enum
from requests.cookies import cookiejar_from_dict

from behave.model import Scenario, ScenarioOutline, Table
from behave.runner import Context

from zapp.features.core.tms.test_culture import TEST_CULTURE_LABEL_NAME

TQL_LABEL_TEMPLATE = 'space = "{space}" AND suit = "test_case" AND label IN ("{label}")'
# TQL_UNIT_TEMPLATE = 'space = "{space}" AND suit = "test_case" AND (unit = "{code}" OR old_jira_key ~ "{code}")'
TQL_UNIT_TEMPLATE = 'space = "{space}" AND suit = "test_case" AND unit = "{code}"'
TQL_OLD_JIRA_KEY_TEMPLATE = (
    'space = "{space}" AND suit = "test_case" AND old_jira_key ~ "{code}"'
)

TAG_SEARCH_PATTERN = r"%s:[^:]+"
FONT_SIZE = 12

AC21_API_COOKIES = cookiejar_from_dict({"api_swtr_as21": "true"})

allure_priority_mapping = {
    "blocker": "blocker",
    "critical": "critical",
    "normal": "major",
    "minor": "minor",
    "trivial": "trivial",
}


class TooManyTestCasesException(Exception):
    pass


class TooManyTagsException(Exception):
    pass


class NoLabelProvidedException(Exception):
    pass


class ScenarioTag(Enum):
    TMS = "allure.link.tms"
    OWNER = "allure.label.owner"
    LABEL = TEST_CULTURE_LABEL_NAME

    def find(self, tags) -> str | None:
        matches = [
            tag for tag in tags if re.match(TAG_SEARCH_PATTERN % self.value, tag)
        ]

        match = _get_one_match(matches)

        if match:
            return match.split(":")[-1]


def get_priority(tags) -> str:
    matches = [tag for tag in tags if tag in allure_priority_mapping]

    match = _get_one_match(matches) or "normal"  # Значение по умолчанию
    return allure_priority_mapping[match]


def _get_one_match(matches: list[str]) -> str | None:
    if len(matches) > 1:
        raise TooManyTagsException(f"Найдено несколько тегов: {matches}")

    if len(matches) == 1:
        return matches[0]


def get_scenario(context: Context) -> Scenario | ScenarioOutline:
    if context.active_outline:
        for scenario in context.feature.scenarios:
            if scenario.tags == context.scenario.tags:
                return scenario
    else:
        return context.scenario


def get_column_widths(table: Table) -> list[int]:
    """Подсчет максимальной длины столбца таблицы"""
    rows = [table.headings] + [row.cells for row in table.rows]
    widths = [[len(str(cell)) for cell in row] for row in rows]
    return [max(column) * FONT_SIZE for column in zip(*widths)]
