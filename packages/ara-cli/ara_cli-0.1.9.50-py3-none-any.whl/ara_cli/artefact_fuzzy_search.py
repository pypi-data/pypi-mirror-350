import difflib
from typing import Optional


def suggest_close_names(artefact_name: str, all_artefact_names: list[str], message: str):
    closest_matches = difflib.get_close_matches(artefact_name, all_artefact_names, cutoff=0.5)
    print(message)
    if not closest_matches:
        return
    print("Closest matches:")
    for match in closest_matches:
        print(f"  - {match}")


def suggest_close_name_matches(artefact_name: str, all_artefact_names: list[str]):
    message = f"No match found for artefact with name '{artefact_name}'"

    suggest_close_names(
        artefact_name=artefact_name,
        all_artefact_names=all_artefact_names,
        message=message
    )


def suggest_close_name_matches_for_parent(artefact_name: str, all_artefact_names: list[str], parent_name: str):
    message = f"No match found for parent of '{artefact_name}' with name '{parent_name}'"

    suggest_close_names(
        artefact_name=artefact_name,
        all_artefact_names=all_artefact_names,
        message=message
    )


def find_closest_name_match(artefact_name: str, all_artefact_names: list[str]) -> Optional[str]:
    closest_matches = difflib.get_close_matches(artefact_name, all_artefact_names, cutoff=0.5, n=1)
    if not closest_matches:
        return None
    closest_match = closest_matches[0]
    return closest_match
