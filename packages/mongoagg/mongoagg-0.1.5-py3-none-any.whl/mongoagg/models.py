from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class Expr:
    """Helper class for building MongoDB aggregation expressions."""
    
    @staticmethod
    def eq(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $eq expression."""
        return {"$eq": [a, b]}
    
    @staticmethod
    def ne(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $ne expression."""
        return {"$ne": [a, b]}
    
    @staticmethod
    def gt(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $gt expression."""
        return {"$gt": [a, b]}
    
    @staticmethod
    def gte(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $gte expression."""
        return {"$gte": [a, b]}
    
    @staticmethod
    def lt(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $lt expression."""
        return {"$lt": [a, b]}
    
    @staticmethod
    def lte(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $lte expression."""
        return {"$lte": [a, b]}
    
    @staticmethod
    def in_(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $in expression."""
        return {"$in": [a, b]}
    
    @staticmethod
    def nin(a: Any, b: List[Any]) -> Dict[str, List[Any]]:
        """Returns a $nin expression."""
        return {"$nin": [a, b]}
    
    @staticmethod
    def and_(*args: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Returns a $and expression."""
        return {"$and": list(args)}
    
    @staticmethod
    def or_(*args: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Returns a $or expression."""
        return {"$or": list(args)}
    
    @staticmethod
    def not_(expr: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Returns a $not expression."""
        return {"$not": expr}
    
    @staticmethod
    def cond(if_: Dict[str, Any], then: Any, else_: Any) -> Dict[str, Dict[str, Any]]:
        """Returns a $cond expression."""
        return {"$cond": {"if": if_, "then": then, "else": else_}}
    
    @staticmethod
    def if_null(expr: Any, replacement: Any) -> Dict[str, List[Any]]:
        """Returns a $ifNull expression."""
        return {"$ifNull": [expr, replacement]}
    
    @staticmethod
    def coalesce(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $coalesce expression."""
        return {"$coalesce": list(args)}
    
    @staticmethod
    def sum(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $sum expression."""
        return {"$sum": list(args)}
    
    @staticmethod
    def avg(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $avg expression."""
        return {"$avg": list(args)}
    
    @staticmethod
    def min(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $min expression."""
        return {"$min": list(args)}
    
    @staticmethod
    def max(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $max expression."""
        return {"$max": list(args)}
    
    @staticmethod
    def push(expr: Any) -> Dict[str, Any]:
        """Returns a $push expression."""
        return {"$push": expr}
    
    @staticmethod
    def add_to_set(expr: Any) -> Dict[str, Any]:
        """Returns a $addToSet expression."""
        return {"$addToSet": expr}
    
    @staticmethod
    def first(expr: Any) -> Dict[str, Any]:
        """Returns a $first expression."""
        return {"$first": expr}
    
    @staticmethod
    def last(expr: Any) -> Dict[str, Any]:
        """Returns a $last expression."""
        return {"$last": expr}
    
    @staticmethod
    def array_elem_at(array: Any, idx: int) -> Dict[str, List[Any]]:
        """Returns a $arrayElemAt expression."""
        return {"$arrayElemAt": [array, idx]}
    
    @staticmethod
    def concat(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $concat expression."""
        return {"$concat": list(args)}
    
    @staticmethod
    def substr(string: Any, start: int, length: int) -> Dict[str, List[Any]]:
        """Returns a $substr expression."""
        return {"$substr": [string, start, length]}
    
    @staticmethod
    def to_lower(expr: Any) -> Dict[str, Any]:
        """Returns a $toLower expression."""
        return {"$toLower": expr}
    
    @staticmethod
    def to_upper(expr: Any) -> Dict[str, Any]:
        """Returns a $toUpper expression."""
        return {"$toUpper": expr}
    
    @staticmethod
    def strcasecmp(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $strcasecmp expression."""
        return {"$strcasecmp": [a, b]}
    
    @staticmethod
    def date_from_string(date_string: str, format: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Returns a $dateFromString expression."""
        expr = {"dateString": date_string}
        if format:
            expr["format"] = format
        return {"$dateFromString": expr}
    
    @staticmethod
    def date_to_string(date: Any, format: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Returns a $dateToString expression."""
        expr = {"date": date}
        if format:
            expr["format"] = format
        return {"$dateToString": expr}
    
    @staticmethod
    def year(date: Any) -> Dict[str, Any]:
        """Returns a $year expression."""
        return {"$year": date}
    
    @staticmethod
    def month(date: Any) -> Dict[str, Any]:
        """Returns a $month expression."""
        return {"$month": date}
    
    @staticmethod
    def day_of_month(date: Any) -> Dict[str, Any]:
        """Returns a $dayOfMonth expression."""
        return {"$dayOfMonth": date}
    
    @staticmethod
    def hour(date: Any) -> Dict[str, Any]:
        """Returns a $hour expression."""
        return {"$hour": date}
    
    @staticmethod
    def minute(date: Any) -> Dict[str, Any]:
        """Returns a $minute expression."""
        return {"$minute": date}
    
    @staticmethod
    def second(date: Any) -> Dict[str, Any]:
        """Returns a $second expression."""
        return {"$second": date}
    
    @staticmethod
    def millisecond(date: Any) -> Dict[str, Any]:
        """Returns a $millisecond expression."""
        return {"$millisecond": date}
    
    @staticmethod
    def day_of_week(date: Any) -> Dict[str, Any]:
        """Returns a $dayOfWeek expression."""
        return {"$dayOfWeek": date}
    
    @staticmethod
    def day_of_year(date: Any) -> Dict[str, Any]:
        """Returns a $dayOfYear expression."""
        return {"$dayOfYear": date}
    
    @staticmethod
    def week(date: Any) -> Dict[str, Any]:
        """Returns a $week expression."""
        return {"$week": date}
    
    @staticmethod
    def iso_week(date: Any) -> Dict[str, Any]:
        """Returns a $isoWeek expression."""
        return {"$isoWeek": date}
    
    @staticmethod
    def iso_day_of_week(date: Any) -> Dict[str, Any]:
        """Returns a $isoDayOfWeek expression."""
        return {"$isoDayOfWeek": date}
    
    @staticmethod
    def iso_year(date: Any) -> Dict[str, Any]:
        """Returns a $isoYear expression."""
        return {"$isoYear": date}
    
    @staticmethod
    def size(array: Any) -> Dict[str, Any]:
        """Returns a $size expression."""
        return {"$size": array}
    
    @staticmethod
    def slice(array: Any, n: int) -> Dict[str, List[Any]]:
        """Returns a $slice expression."""
        return {"$slice": [array, n]}
    
    @staticmethod
    def map(input: Any, as_: str, in_: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Returns a $map expression."""
        return {"$map": {"input": input, "as": as_, "in": in_}}
    
    @staticmethod
    def filter(input: Any, as_: str, cond: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Returns a $filter expression."""
        return {"$filter": {"input": input, "as": as_, "cond": cond}}
    
    @staticmethod
    def reduce(input: Any, initial_value: Any, in_: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Returns a $reduce expression."""
        return {"$reduce": {"input": input, "initialValue": initial_value, "in": in_}}
    
    @staticmethod
    def zip(inputs: List[Any], use_longest_length: bool = False, defaults: Optional[List[Any]] = None) -> Dict[str, Dict[str, Any]]:
        """Returns a $zip expression."""
        expr = {"inputs": inputs, "useLongestLength": use_longest_length}
        if defaults:
            expr["defaults"] = defaults
        return {"$zip": expr}
    
    @staticmethod
    def in_range(expr: Any, start: Any, end: Any, inclusive: bool = True) -> Dict[str, Dict[str, Any]]:
        """Returns a $inRange expression."""
        return {"$inRange": {"expr": expr, "start": start, "end": end, "inclusive": inclusive}}
    
    @staticmethod
    def index_of_array(array: Any, search: Any, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, Dict[str, Any]]:
        """Returns a $indexOfArray expression."""
        expr = {"array": array, "search": search}
        if start is not None:
            expr["start"] = start
        if end is not None:
            expr["end"] = end
        return {"$indexOfArray": expr}
    
    @staticmethod
    def index_of_bytes(string: Any, substring: Any, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, Dict[str, Any]]:
        """Returns a $indexOfBytes expression."""
        expr = {"string": string, "substring": substring}
        if start is not None:
            expr["start"] = start
        if end is not None:
            expr["end"] = end
        return {"$indexOfBytes": expr}
    
    @staticmethod
    def index_of_cp(string: Any, substring: Any, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, Dict[str, Any]]:
        """Returns a $indexOfCP expression."""
        expr = {"string": string, "substring": substring}
        if start is not None:
            expr["start"] = start
        if end is not None:
            expr["end"] = end
        return {"$indexOfCP": expr}
    
    @staticmethod
    def split(string: Any, delimiter: Any) -> Dict[str, List[Any]]:
        """Returns a $split expression."""
        return {"$split": [string, delimiter]}
    
    @staticmethod
    def str_len_bytes(string: Any) -> Dict[str, Any]:
        """Returns a $strLenBytes expression."""
        return {"$strLenBytes": string}
    
    @staticmethod
    def str_len_cp(string: Any) -> Dict[str, Any]:
        """Returns a $strLenCP expression."""
        return {"$strLenCP": string}
    
    @staticmethod
    def substr_bytes(string: Any, start: int, count: int) -> Dict[str, List[Any]]:
        """Returns a $substrBytes expression."""
        return {"$substrBytes": [string, start, count]}
    
    @staticmethod
    def substr_cp(string: Any, start: int, count: int) -> Dict[str, List[Any]]:
        """Returns a $substrCP expression."""
        return {"$substrCP": [string, start, count]}
    
    @staticmethod
    def to_decimal(expr: Any) -> Dict[str, Any]:
        """Returns a $toDecimal expression."""
        return {"$toDecimal": expr}
    
    @staticmethod
    def to_double(expr: Any) -> Dict[str, Any]:
        """Returns a $toDouble expression."""
        return {"$toDouble": expr}
    
    @staticmethod
    def to_int(expr: Any) -> Dict[str, Any]:
        """Returns a $toInt expression."""
        return {"$toInt": expr}
    
    @staticmethod
    def to_long(expr: Any) -> Dict[str, Any]:
        """Returns a $toLong expression."""
        return {"$toLong": expr}
    
    @staticmethod
    def to_object_id(expr: Any) -> Dict[str, Any]:
        """Returns a $toObjectId expression."""
        return {"$toObjectId": expr}
    
    @staticmethod
    def to_string(expr: Any) -> Dict[str, Any]:
        """Returns a $toString expression."""
        return {"$toString": expr}
    
    @staticmethod
    def trunc(expr: Any) -> Dict[str, Any]:
        """Returns a $trunc expression."""
        return {"$trunc": expr}
    
    @staticmethod
    def ceil(expr: Any) -> Dict[str, Any]:
        """Returns a $ceil expression."""
        return {"$ceil": expr}
    
    @staticmethod
    def floor(expr: Any) -> Dict[str, Any]:
        """Returns a $floor expression."""
        return {"$floor": expr}
    
    @staticmethod
    def round(expr: Any, place: Optional[int] = None) -> Dict[str, Any]:
        """Returns a $round expression."""
        if place is not None:
            return {"$round": [expr, place]}
        return {"$round": expr}
    
    @staticmethod
    def abs(expr: Any) -> Dict[str, Any]:
        """Returns a $abs expression."""
        return {"$abs": expr}
    
    @staticmethod
    def exp(expr: Any) -> Dict[str, Any]:
        """Returns a $exp expression."""
        return {"$exp": expr}
    
    @staticmethod
    def ln(expr: Any) -> Dict[str, Any]:
        """Returns a $ln expression."""
        return {"$ln": expr}
    
    @staticmethod
    def log10(expr: Any) -> Dict[str, Any]:
        """Returns a $log10 expression."""
        return {"$log10": expr}
    
    @staticmethod
    def sqrt(expr: Any) -> Dict[str, Any]:
        """Returns a $sqrt expression."""
        return {"$sqrt": expr}
    
    @staticmethod
    def pow(base: Any, exponent: Any) -> Dict[str, List[Any]]:
        """Returns a $pow expression."""
        return {"$pow": [base, exponent]}
    
    @staticmethod
    def mod(dividend: Any, divisor: Any) -> Dict[str, List[Any]]:
        """Returns a $mod expression."""
        return {"$mod": [dividend, divisor]}
    
    @staticmethod
    def add(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $add expression."""
        return {"$add": list(args)}
    
    @staticmethod
    def subtract(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $subtract expression."""
        return {"$subtract": [a, b]}
    
    @staticmethod
    def multiply(*args: Any) -> Dict[str, List[Any]]:
        """Returns a $multiply expression."""
        return {"$multiply": list(args)}
    
    @staticmethod
    def divide(a: Any, b: Any) -> Dict[str, List[Any]]:
        """Returns a $divide expression."""
        return {"$divide": [a, b]}

    
    @staticmethod
    def remove() -> str:
        """Returns $$REMOVE for removing fields in projections."""
        return "$$REMOVE"
    
    @staticmethod
    def keep() -> str:
        """Returns $$KEEP for keeping fields in redact operations."""
        return "$$KEEP"
    
    @staticmethod
    def descend() -> str:
        """Returns $$DESCEND for descending into fields in redact operations."""
        return "$$DESCEND"
    
    @staticmethod
    def prune() -> str:
        """Returns $$PRUNE for pruning fields in redact operations."""
        return "$$PRUNE"
    
    @staticmethod
    def root() -> str:
        """Returns $$ROOT for accessing the root document."""
        return "$$ROOT"
    
    @staticmethod
    def current() -> str:
        """Returns $$CURRENT for accessing the current document."""
        return "$$CURRENT"
    
    @staticmethod
    def when(condition: Dict[str, Any]) -> "ConditionBuilder":
        """
        Starts building a conditional expression.
        
        Example:
            Expr.when(Expr.eq("$status", "active"))
                .then("$field")
                .otherwise(Expr.remove())
        """
        return ConditionBuilder(condition)

class ConditionBuilder:
    """Builder for conditional expressions."""
    
    def __init__(self, condition: Dict[str, Any]):
        self._condition = condition
        self._then = None
        self._else = None
    
    def then(self, value: Any) -> "ConditionBuilder":
        """Sets the value to return when the condition is true."""
        self._then = value
        return self
    
    def otherwise(self, value: Any) -> Dict[str, Dict[str, Any]]:
        """Sets the value to return when the condition is false and builds the expression."""
        self._else = value
        return Expr.cond(self._condition, self._then, self._else)

class Stage(BaseModel):
    """Base class for MongoDB aggregation stages."""
    def to_mongo(self) -> Dict[str, Any]:
        """Convert the stage to MongoDB aggregation format."""
        raise NotImplementedError("Each stage type must implement to_mongo()")

class MatchStage(Stage):
    """Model for $match stage."""
    match: Dict[str, Any] = Field(..., description="Query criteria to match documents")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$match": self.match}

class ProjectStage(Stage):
    """Model for $project stage."""
    project: Dict[str, Any] = Field(..., description="Field specifications to include/exclude")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$project": self.project}

class SortStage(Stage):
    """Model for $sort stage."""
    sort: Dict[str, int] = Field(..., description="Field specifications with sort direction (1 for ascending, -1 for descending)")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$sort": self.sort}

class LimitStage(Stage):
    """Model for $limit stage."""
    limit: int = Field(..., ge=0, description="Maximum number of documents to return")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$limit": self.limit}

class SkipStage(Stage):
    """Model for $skip stage."""
    skip: int = Field(..., ge=0, description="Number of documents to skip")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$skip": self.skip}

class UnwindStage(Stage):
    """Model for $unwind stage."""
    path: str = Field(..., description="The array field path to unwind")
    preserve_null_and_empty: bool = Field(default=True, description="Whether to preserve documents with null or empty arrays")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {
            "$unwind": {
                "path": self.path,
                "preserveNullAndEmptyArrays": self.preserve_null_and_empty
            }
        }

class GroupStage(Stage):
    """Model for $group stage."""
    id_field: Any = Field(..., description="The group key expression")
    accumulators: Dict[str, Any] = Field(default_factory=dict, description="Accumulator expressions for grouped values")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$group": {"_id": self.id_field, **self.accumulators}}

class AddFieldsStage(Stage):
    """Model for $addFields stage."""
    fields: Dict[str, Any] = Field(..., description="New field specifications")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$addFields": self.fields}

class ReplaceRootStage(Stage):
    """Model for $replaceRoot stage."""
    new_root: Dict[str, Any] = Field(..., description="The new root document expression")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$replaceRoot": {"newRoot": self.new_root}}

class LookupStage(Stage):
    """Model for $lookup stage."""
    from_: str = Field(..., description="The collection to join with")
    as_: str = Field(..., description="The output array field name")
    local_field: Optional[str] = Field(None, description="The field from the input documents")
    foreign_field: Optional[str] = Field(None, description="The field from the documents of the 'from' collection")
    let_: Optional[Dict[str, Any]] = Field(None, description="Variables to use in the pipeline field")
    pipeline: Optional[List[Dict[str, Any]]] = Field(None, description="The pipeline to run on the joined collection")
    
    def to_mongo(self) -> Dict[str, Any]:
        lookup: Dict[str, Any] = {
            "from": self.from_,
            "as": self.as_
        }
        if self.pipeline is not None:
            lookup["let"] = self.let_
            lookup["pipeline"] = self.pipeline
        else:
            lookup["localField"] = self.local_field
            lookup["foreignField"] = self.foreign_field
        return {"$lookup": lookup}

class FacetStage(Stage):
    """Model for $facet stage."""
    pipelines: Dict[str, List[Dict[str, Any]]] = Field(..., description="Named aggregation pipelines")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$facet": self.pipelines}

class RedactStage(Stage):
    """Model for $redact stage."""
    condition: Dict[str, Any] = Field(..., description="The condition expression")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$redact": self.condition}

class CommentStage(Stage):
    """Model for $comment stage."""
    text: str = Field(..., description="The comment text to add to the pipeline")
    
    def to_mongo(self) -> Dict[str, Any]:
        return {"$comment": self.text}

# Union type for all possible stages
AggregationStage = Union[
    MatchStage,
    ProjectStage,
    SortStage,
    LimitStage,
    SkipStage,
    UnwindStage,
    GroupStage,
    AddFieldsStage,
    ReplaceRootStage,
    LookupStage,
    FacetStage,
    RedactStage,
    CommentStage
]

class Pipeline(BaseModel):
    """Model for MongoDB aggregation pipeline."""
    stages: List[Dict[str, Any]] = Field(default_factory=list, description="List of aggregation stages") 