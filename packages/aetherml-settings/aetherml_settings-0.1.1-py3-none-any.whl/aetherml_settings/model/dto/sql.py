from pydantic import BaseModel, field_validator
from typing import List, Optional
import sqlparse # Make sure to install sqlparse: pip install sqlparse

def _validate_sql_structure(value: str, allowed_types: List[str], forbidden_types: Optional[List[str]] = None, type_description: str = "statement") -> str:
    if not value.strip():
        raise ValueError(f"SQL {type_description} cannot be empty.")
    
    forbidden_types = forbidden_types or []

    try:
        parsed_statements = sqlparse.parse(value)
        if not parsed_statements:
            raise ValueError(f"Invalid SQL: Unable to parse {type_description}.")

        stmt = parsed_statements[0]
        statement_type = stmt.get_type().upper()

        if isinstance(stmt.tokens[0], sqlparse.tokens.Error):
            raise ValueError(f"Invalid SQL: {type_description.capitalize()} contains syntax errors.")

        if statement_type in forbidden_types:
            raise ValueError(f"{statement_type} {type_description}s are not allowed.")

        if statement_type not in allowed_types:
            allowed_str = ", ".join(allowed_types)
            raise ValueError(f"Only {allowed_str} {type_description}s are allowed. Found: {statement_type}")
        
        return value
    except ValueError: # Re-raise ValueErrors from our checks
        raise
    except Exception as e:
        raise ValueError(f"SQL validation failed for {type_description}: {e}")

def validate_select_query_str(value: str) -> str:
    return _validate_sql_structure(
        value,
        allowed_types=["SELECT"],
        forbidden_types=["UPDATE", "DELETE"],
        type_description="query"
    )

def validate_insert_statement_str(value: str) -> str:
    return _validate_sql_structure(
        value,
        allowed_types=["INSERT"],
        forbidden_types=["UPDATE", "DELETE", "SELECT"], # Also forbid SELECT for insert statements
        type_description="statement"
    )

class SQLStatement(BaseModel):
    statement: str

    @field_validator('statement')
    @classmethod
    def validate_statement_field(cls, value: str) -> str:
        return validate_select_query_str(value)

class SQLInsertStatement(BaseModel):
    statement: str

    @field_validator('statement')
    @classmethod
    def validate_statement_field(cls, value: str) -> str:
        return validate_insert_statement_str(value)

# Example usage (for testing):
# try:
#     SQLStatement(statement="SELECT * FROM users WHERE id = 1 GROUP BY name")
#     print("Valid SELECT passed SQLStatement")
#     SQLInsertStatement(statement="INSERT INTO users (name) VALUES ('test')")
#     print("Valid INSERT passed SQLInsertStatement")
# except ValueError as e:
#     print(f"Validation Error: {e}")

# try:
#     SQLStatement(statement="INSERT INTO users (name) VALUES ('test')") # Should fail for SQLStatement
# except ValueError as e:
#     print(f"Expected fail for SQLStatement (INSERT): {e}")

# try:
#     SQLInsertStatement(statement="SELECT * FROM users") # Should fail for SQLInsertStatement
# except ValueError as e:
#     print(f"Expected fail for SQLInsertStatement (SELECT): {e}")

# try:
#     SQLStatement(statement="UPDATE users SET name = 'new' WHERE id = 1") # Should fail
# except ValueError as e:
#     print(f"Expected fail for SQLStatement (UPDATE): {e}")
