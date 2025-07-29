pub struct DocumentLink {
    pub target: tower_lsp::lsp_types::Url,
    pub range: tombi_text::Range,
    pub tooltip: String,
}

impl Into<tower_lsp::lsp_types::DocumentLink> for DocumentLink {
    fn into(self) -> tower_lsp::lsp_types::DocumentLink {
        tower_lsp::lsp_types::DocumentLink {
            range: self.range.into(),
            target: Some(self.target),
            tooltip: Some(self.tooltip),
            data: None,
        }
    }
}
