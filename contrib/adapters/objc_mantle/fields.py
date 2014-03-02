from models.fields import *

# Could potentially do something else, like monkey-patch
# the Field classes when this module is imported

# A mapping from Field classes to ObjC properties
# All of these receive {{ field_name }}; afterward
FIELD_PROPERTIES = {
    GUIDField:    '@property (nonatomic, strong) NSString *',
    DateField:    '@property (nonatomic, strong) NSDate *',
    UIntField:    '@property (nonatomic, assign) UInt32 ',
    FloatField:   '@property (nonatomic, assign) float ',
    ArrayField:   '@property (nonatomic, strong) NSArray *',
    StringField:  '@property (nonatomic, strong) NSString *',
    BooleanField: '@property (nonatomic, assign) BOOL ',
    UrlField:     '@property (nonatomic, strong) NSURL *',
    # a class?
    # Needs to include the Enum name
    EnumField: '',
    # a class?
    # Needs to include the ObjC class name
    EmbeddedField: '',
}
