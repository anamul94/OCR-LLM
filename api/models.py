from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Enums
class Category(str, Enum):
    """Enum for image analysis categories."""
    FOOD = "food"
    MEDICAL = "medical"

# Base Models
class BaseResponse(BaseModel):
    """Base response model with common fields."""
    status: bool = Field(description="Indicates whether the request was successful.")
    message: str = Field(description="A descriptive message about the response.")

# Food Analysis Models
class NutritionValue(BaseModel):
    """Represents a specific nutritional component of a food item."""
    name: str = Field(description="The name of the nutritional component (e.g., Protein, Calories, Carbohydrates).")
    value: float = Field(description="The numerical value of the nutritional component per serving.")
    unit: str = Field(description="The unit of measurement for the nutrition value (e.g., kcal, g, mg).")

class FoodInformation(BaseModel):
    """Stores detailed information about a food item."""
    name: str = Field(description="The name of the food item (e.g., Apple, Chicken Breast).")
    nutritions: List[NutritionValue] = Field(description="A list of nutritional values associated with the food item.")
    serving_size: float = Field(description="The standard serving size of the food item in grams (g) or milliliters (ml).")
    serving_unit: str = Field(description="The unit of measurement for the serving size (e.g., g, ml).")

class FoodResponse(BaseResponse):
    """Defines the structure of the food API response."""
    data: List[FoodInformation] = Field(default_factory=list, description="A list of food items with nutritional information.")

# Medical Analysis Models
class PatientDetails(BaseModel):
    """Patient information from medical reports."""
    name: Optional[str] = Field(None, description="Patient name if available.")
    age: Optional[int] = Field(None, description="Patient age if available.")
    gender: Optional[str] = Field(None, description="Patient gender if available.")

class TestResult(BaseModel):
    """Individual test result with reference values."""
    value: str = Field(description="The measured value of the test result.")
    reference_range: str = Field(description="The normal reference range for the test.")
    status: str = Field(description="Status of the result (Normal, High, Low, etc.).")

class DiagnosticTest(BaseModel):
    """A diagnostic test with its results."""
    test_name: str = Field(description="Name of the diagnostic test.")
    results: Dict[str, TestResult] = Field(description="Dictionary of test results.")
    observations: Optional[str] = Field(None, description="Clinical observations for this test.")

class MedicalResponse(BaseResponse):
    """Defines the structure of the medical API response."""
    data: Dict[str, Any] = Field(default_factory=dict, description="Structured medical report data.")

# Error Response Model
class ErrorResponse(BaseResponse):
    """Error response with optional debug information."""
    data: List = Field(default_factory=list)
    debug_info: Optional[Dict[str, Any]] = Field(None, description="Debug information, only included in debug mode.")
