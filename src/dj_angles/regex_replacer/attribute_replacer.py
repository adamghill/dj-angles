import logging
import re

from dj_angles.htmls import find_character, get_outer_html
from dj_angles.regex_replacer.objects import Replacement
from dj_angles.settings import get_setting
from dj_angles.strings import dequotify

logger = logging.getLogger(__name__)


def get_attribute_replacements(html: str) -> list[Replacement]:
    """Get a list of attribute replacements based on the template HTML.

    Args:
        param html: Template HTML.

    Returns:
        A list of `Replacement` where `original` is the existing element, e.g. "<div dj-if="True"></div>"
        and `replacement` is the replacement string, e.g. "{% if True %}<div></div>{% endif %}".
    """

    replacements: list[Replacement] = []

    initial_attribute_regex = get_setting("initial_attribute_regex", default=r"(dj-)")
    if_attribute_regex = re.compile(rf"{initial_attribute_regex}if")
    elif_attribute_regex = re.compile(rf"{initial_attribute_regex}elif")
    else_attribute_regex = re.compile(rf"{initial_attribute_regex}else")
    endif_attribute_regex = re.compile(rf"({initial_attribute_regex}endif|{initial_attribute_regex}fi)")

    for match in re.finditer(
        rf"\s(({initial_attribute_regex}if|{initial_attribute_regex}elif)=|{initial_attribute_regex}else|{initial_attribute_regex}endif|{initial_attribute_regex}fi)",
        html,
    ):
        dj_attribute = (match.groups()[1] or match.groups()[0]).strip()

        attribute_start_idx = match.start()

        value_start_idx = match.end()
        value_end_idx = find_character(html, value_start_idx, character_regex=r"[\s>]")
        value = html[value_start_idx:value_end_idx]
        value = dequotify(value)

        conditional_start_tag = ""
        condition_end_tag = ""
        is_explicit_endif = False
        is_implicit_endif = False

        if if_attribute_regex.search(dj_attribute):
            conditional_start_tag = f"{{% if {value} %}}"
            condition_end_tag = "{% endif %}"
        elif elif_attribute_regex.search(dj_attribute):
            conditional_start_tag = f"{{% elif {value} %}}"
            condition_end_tag = "{% endif %}"
        elif else_attribute_regex.search(dj_attribute):
            conditional_start_tag = "{% else %}"
            condition_end_tag = "{% endif %}"
        elif endif_attribute_regex.search(dj_attribute):
            pass
        else:
            raise AssertionError(f"Unknown attribute: {dj_attribute}")

        # Get the outer HTML of the tag that the attribute is in
        tag_start_idx = find_character(html, value_start_idx, "<", reverse=True)
        tag = get_outer_html(html, tag_start_idx)

        if not tag:
            raise AssertionError("Tag could not be found")

        if tag.is_end and endif_attribute_regex.search(tag.html):
            # Remove the explicit endif from the end tag and mark it and the previous tag as having an explicit endif
            replacement_idx = len(replacements) - 1

            while replacement_idx >= 0:
                previous_replacement = replacements[replacement_idx]

                if previous_replacement.replacement.endswith("{% endif %}"):
                    previous_replacement.replacement = previous_replacement.replacement[:-11]

                if if_attribute_regex.search(previous_replacement.original):
                    break

                replacement_idx -= 1

            replacement_html = endif_attribute_regex.sub("", tag.html).replace(" >", ">") + "{% endif %}"

            new_replacement = Replacement(
                original=tag.html,
                replacement=replacement_html,
                tag=tag,
                keep_endif=True,
                tag_start_idx=tag_start_idx,
            )

            replacements.append(new_replacement)
            continue

        if tag.outer_html is None:
            raise AttributeError("Unknown outer html for tag")

        if replacements:
            previous_replacement = replacements[-1]

            if previous_replacement.tag.outer_html is None:
                raise AssertionError("Previous tag has no outer html")

            if previous_replacement.tag_start_idx > -1 and tag_start_idx > previous_replacement.tag_start_idx:
                check_idx = previous_replacement.tag_start_idx + len(previous_replacement.tag.outer_html)

                if tag_start_idx < check_idx:
                    is_implicit_endif = True

        # Remove the dj_angles attribute from the tag's HTML
        replacement_html = (
            tag.outer_html[: attribute_start_idx - tag_start_idx] + tag.outer_html[value_end_idx - tag_start_idx :]
        )

        if elif_attribute_regex.search(dj_attribute) or else_attribute_regex.search(dj_attribute):
            # Check that dj-elif and dj-else attributes are used in a conditional block
            if not replacements:
                raise AssertionError(f"Invalid use of {dj_attribute} outside of a conditional block")

            replacement_idx = len(replacements) - 1

            while replacement_idx >= 0:
                previous_replacement = replacements[replacement_idx]

                if not previous_replacement.keep_endif:
                    if else_attribute_regex.search(dj_attribute):
                        if not (
                            elif_attribute_regex.search(previous_replacement.original)
                            or if_attribute_regex.search(previous_replacement.original)
                        ):
                            raise AssertionError(f"Invalid use of {dj_attribute} attribute")
                    elif elif_attribute_regex.search(dj_attribute):
                        if not (
                            if_attribute_regex.search(previous_replacement.original)
                            or elif_attribute_regex.search(previous_replacement.original)
                        ):
                            raise AssertionError(f"Invalid use of {dj_attribute} attribute")

                    # Remove {% endif %} from the previous replacement
                    if previous_replacement.replacement.endswith("{% endif %}"):
                        replacements[replacement_idx].original = previous_replacement.original
                        replacements[replacement_idx].replacement = previous_replacement.replacement[:-11]
                        replacements[replacement_idx].tag = previous_replacement.tag
                        replacements[replacement_idx].keep_endif = is_explicit_endif
                        replacements[replacement_idx].tag_start_idx = previous_replacement.tag_start_idx

                        break

                replacement_idx -= 1

        replacement_html = f"{conditional_start_tag}{replacement_html}{condition_end_tag}"
        new_replacement = Replacement(
            original=tag.outer_html,
            replacement=replacement_html,
            tag=tag,
            keep_endif=is_explicit_endif or is_implicit_endif,
            tag_start_idx=tag_start_idx,
        )
        replacements.append(new_replacement)

    # print()
    # for r in replacements:
    #     print(r)
    # print()

    logger.debug("Attribute replacements: %s", replacements)

    return replacements
