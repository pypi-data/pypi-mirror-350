class EntityType:
    def __init__(self, name: str, primary_color: str, secondary_color: str = None):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        if self.secondary_color is None:
            self.secondary_color = primary_color
    
    def to_dict(self):
        return {
            "name": self.name,
            "primaryColor": self.primary_color,
            "secondaryColor": self.secondary_color
        }
    
class Annotation:
    def __init__(self, start: int, end: int, entity_type: str | EntityType, confidence_score: float = -1, text: str = ""):
        self.start = start
        self.end = end
        if isinstance(entity_type, EntityType):
            self.entity_type = entity_type.name
        else:
            self.entity_type = entity_type
        self.confidence_score = confidence_score
        self.text = text

    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "entityType": self.entity_type,
            "confidenceScore": self.confidence_score,
            "text": self.text
        }
    
class AnnotationData:
    def __init__(self, text: str, annotations: list[Annotation]):
        self.text = text
        self.annotations = annotations

    def to_dict(self):
        return {
            "text": self.text,
            "annotations": [a.to_dict() for a in self.annotations]
        }