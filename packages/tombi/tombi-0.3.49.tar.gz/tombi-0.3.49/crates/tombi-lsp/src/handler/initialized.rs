use tower_lsp::lsp_types::{InitializedParams, MessageType};

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_initialized(backend: &Backend, params: InitializedParams) {
    tracing::info!("handle_initialized");
    tracing::trace!(?params);

    if let Err(error) = backend
        .schema_store
        .load_config(&backend.config().await, backend.config_path.as_deref())
        .await
    {
        if let Err(error) = backend
            .client
            .show_message_request(MessageType::ERROR, error.to_string(), None)
            .await
        {
            tracing::error!("{:?}", error);
        }
    }
}
