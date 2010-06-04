class FieldType:
    DF = 0.1
    EF = 0.2
    Bitmap = 0.3
    Final = 0.4
    Counter = 0.5
    DFName = 0.6
    DFList = 0.7
    TransparentEF = 0.8
    FinalRepeated = 0.9
    StructRepeated = 0.01
    ReversedStructRepeated = 0.02

class FinalType:
    Unknown = 0.1
    HexString = 0.2
    Integer = 0.3
    IMSIMCC = 0.4
    RevHexString = 0.5
    MNC = 0.6
    PLMNMCC = 0.7
    DisplayCondition = 0.8
    String = 0.9
    BinaryString = 0.01
    LocationUpdateStatus = 0.02
    OperationMode = 0.03
    Phase = 0.04
    NumRevHexString = 0.05
    TonNpi = 0.06
    SMSStatus = 0.07