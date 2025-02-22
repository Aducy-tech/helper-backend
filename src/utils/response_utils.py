from typing import Type, Dict, List
from fastapi import HTTPException


def get_error_response_schema(description: str) -> dict:
    """
    Creates a standardized error response schema
    """
    return {
        'description': description,
        'content': {
            'application/json': {
                'example': {'detail': description}
            }
        }
    }


def combine_error_responses(
    error_groups: Dict[int, List[Type[HTTPException]]]
) -> dict:
    """
    Combines error descriptions with the same status code.

    Args:
        error_groups: Dictionary where the key is the status code,
                      and the value is a list of exception classes
    """

    responses = {}

    for status_code, exceptions in error_groups.items():
        descriptions = [exc.detail for exc in exceptions]

        responses[status_code] = {
            'description': '\n'.join([
                'Possible errors:',
                *[f'- {desc}' for desc in descriptions]
            ]),
            'content': {
                'application/json': {
                    'examples': {
                        exc.__name__: {
                            'summary': exc.detail,
                            'value': {'detail': exc.detail}
                        } for exc in exceptions
                    }
                }
            }
        }

    return responses
