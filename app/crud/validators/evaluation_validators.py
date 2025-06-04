from exceptions.evaluation_exceptions import DuplicateEstimateError


def already_estimated(
    existing_evaluation,
) -> None:
    if existing_evaluation.scalar_one_or_none():
        raise DuplicateEstimateError()
