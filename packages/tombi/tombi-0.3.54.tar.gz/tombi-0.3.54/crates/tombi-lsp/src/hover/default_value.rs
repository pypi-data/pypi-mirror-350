#[derive(Debug, Clone)]
pub enum DefaultValue {
    Boolean(bool),
    Integer(i64),
    Float(f64),
    String(String),
    OffsetDateTime(String),
    LocalDateTime(String),
    LocalDate(String),
    LocalTime(String),
    Array(Vec<DefaultValue>),
    Table(Vec<(String, DefaultValue)>),
}

impl TryFrom<&tombi_json::Value> for DefaultValue {
    type Error = ();

    fn try_from(value: &tombi_json::Value) -> Result<Self, Self::Error> {
        match value {
            tombi_json::Value::Bool(boolean) => Ok(DefaultValue::Boolean(*boolean)),
            tombi_json::Value::Number(number) => match number {
                tombi_json::Number::Integer(integer) => Ok(DefaultValue::Integer(*integer)),
                tombi_json::Number::Float(float) => Ok(DefaultValue::Float(*float)),
            },
            tombi_json::Value::String(string) => Ok(DefaultValue::String(string.clone())),
            tombi_json::Value::Array(array) => Ok(DefaultValue::Array(
                array.iter().map(|item| item.try_into().unwrap()).collect(),
            )),
            tombi_json::Value::Object(object) => Ok(DefaultValue::Table(
                object
                    .iter()
                    .map(|(key, value)| (key.clone(), value.try_into().unwrap()))
                    .collect(),
            )),
            tombi_json::Value::Null => Err(()),
        }
    }
}

impl std::fmt::Display for DefaultValue {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DefaultValue::Boolean(boolean) => write!(f, "{}", boolean),
            DefaultValue::Integer(integer) => write!(f, "{}", integer),
            DefaultValue::Float(float) => write!(f, "{}", float),
            DefaultValue::String(string) => write!(f, "\"{}\"", string.replace("\"", "\\\"")),
            DefaultValue::OffsetDateTime(offset_date_time) => write!(f, "{}", offset_date_time),
            DefaultValue::LocalDateTime(local_date_time) => write!(f, "{}", local_date_time),
            DefaultValue::LocalDate(local_date) => write!(f, "{}", local_date),
            DefaultValue::LocalTime(local_time) => write!(f, "{}", local_time),
            DefaultValue::Array(array) => {
                write!(f, "[")?;
                for (i, value) in array.iter().enumerate() {
                    if i > 0 {
                        write!(f, ", ")?;
                    }
                    write!(f, "{}", value)?;
                }
                write!(f, "]")
            }
            DefaultValue::Table(table) => {
                write!(f, "{{ ")?;
                for (i, (key, value)) in table.iter().enumerate() {
                    if i > 0 {
                        write!(f, ", ")?;
                    }
                    write!(f, "{}: {}", key, value)?;
                }
                write!(f, " }}")
            }
        }
    }
}
