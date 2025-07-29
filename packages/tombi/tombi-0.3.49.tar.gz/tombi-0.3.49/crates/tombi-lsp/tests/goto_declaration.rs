use tombi_test_lib::project_root_path;

mod goto_declaration_tests {
    use super::*;

    mod cargo_schema {
        use super::*;

        test_goto_declaration!(
            #[tokio::test]
            async fn dependencies_serde_workspace(
                r#"
                [dependencies]
                serde = { workspace█ = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok([project_root_path().join("Cargo.toml")]);
        );

        test_goto_declaration!(
            #[tokio::test]
            async fn dependencies_serde(
                r#"
                [dependencies]
                serde█ = { workspace = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok([project_root_path().join("Cargo.toml")]);
        );

        test_goto_declaration!(
            #[tokio::test]
            async fn workspace_dependencies_tombi_ast(
                r#"
                [workspace.dependencies]
                tombi-ast = { path█ = "crates/tombi-ast" }
                "#,
                project_root_path().join("Cargo.toml"),
            ) -> Ok([]);
        );

        test_goto_declaration!(
            #[tokio::test]
            async fn workspace_members_xtask(
                r#"
                [workspace]
                members = [
                    "xtask█"
                ]
                "#,
                project_root_path().join("Cargo.toml"),
            ) -> Ok([]);
        );
    }

    mod pyproject_uv_schema {
        use super::*;

        test_goto_declaration!(
            #[tokio::test]
            async fn tool_uv_sources_tombi_beta(
                r#"
                [tool.uv.sources]
                tombi-beta█ = { workspace = true }
                "#,
                project_root_path().join("python/tombi-beta/pyproject.toml"),
            ) -> Ok([project_root_path().join("pyproject.toml")]);
        );

        test_goto_declaration!(
            #[tokio::test]
            async fn tool_uv_sources_tombi_beta_workspace(
                r#"
                [tool.uv.sources]
                tombi-beta = { workspace█ = true }
                "#,
                project_root_path().join("python/tombi-beta/pyproject.toml"),
            ) -> Ok([project_root_path().join("pyproject.toml")]);
        );
    }

    #[macro_export]
    macro_rules! test_goto_declaration {
        (#[tokio::test] async fn $name:ident(
            $source:expr,
            $file_path:expr,
        ) -> Ok([$($expected_file_path:expr),*$(,)?]);) => {
            #[tokio::test]
            async fn $name() -> Result<(), Box<dyn std::error::Error>> {
                use tombi_lsp::handler::{handle_did_open, handle_goto_declaration};
                use tombi_lsp::Backend;
                use tower_lsp::{
                    lsp_types::{
                        DidOpenTextDocumentParams, GotoDefinitionParams, GotoDefinitionResponse,
                        PartialResultParams, TextDocumentIdentifier, TextDocumentItem,
                        TextDocumentPositionParams, Url, WorkDoneProgressParams,
                    },
                    LspService,
                };

                tombi_test_lib::init_tracing();

                let (service, _) = LspService::new(|client| {
                    Backend::new(client, &tombi_lsp::backend::Options::default())
                });

                let backend = service.inner();

                let toml_file_url = Url::from_file_path($file_path).expect("failed to convert file path to URL");

                let mut toml_text = textwrap::dedent($source).trim().to_string();
                let Some(index) = toml_text.as_str().find("█") else {
                    return Err("failed to find position marker (█) in the test data".into());
                };
                toml_text.remove(index);

                handle_did_open(
                    backend,
                    DidOpenTextDocumentParams {
                        text_document: TextDocumentItem {
                            uri: toml_file_url.clone(),
                            language_id: "toml".to_string(),
                            version: 0,
                            text: toml_text.clone(),
                        },
                    },
                )
                .await;

                let params = GotoDefinitionParams {
                    text_document_position_params: TextDocumentPositionParams {
                        text_document: TextDocumentIdentifier { uri: toml_file_url },
                        position: (tombi_text::Position::default()
                            + tombi_text::RelativePosition::of(&toml_text[..index]))
                        .into(),
                    },
                    work_done_progress_params: WorkDoneProgressParams::default(),
                    partial_result_params: PartialResultParams::default(),
                };

                let Ok(result) = handle_goto_declaration(&backend, params).await else {
                    return Err("failed to handle goto_declaration".into());
                };

                tracing::debug!("goto_declaration result: {:#?}", result);

                let expected_paths: Vec<std::path::PathBuf> = vec![$($expected_file_path.to_owned()),*];

                match result {
                    Some(def_links) => {
                        match def_links {
                            GotoDefinitionResponse::Link(links) => {
                                assert!(!links.is_empty(), "Definition links were returned but empty");
                                let target_paths: Vec<_> = links.iter()
                                    .map(|link| link.target_uri.to_file_path()
                                        .expect("Failed to convert URL to file path"))
                                    .collect();

                                pretty_assertions::assert_eq!(
                                    target_paths,
                                    expected_paths,
                                    "Definition links point to unexpected schema paths\nExpected: {:?}\nActual: {:?}",
                                    expected_paths,
                                    target_paths
                                );
                            },
                            GotoDefinitionResponse::Scalar(location) => {
                                let target_path = location.uri.to_file_path()
                                    .expect("Failed to convert URL to file path");

                                pretty_assertions::assert_eq!(
                                    vec![target_path.clone()],
                                    expected_paths,
                                    "Definition link points to an unexpected schema path\nExpected: {:?}\nActual: {:?}",
                                    expected_paths,
                                    target_path
                                );
                            },
                            GotoDefinitionResponse::Array(locations) => {
                                assert!(!locations.is_empty(), "Definition locations were returned but empty");
                                let target_paths: Vec<_> = locations.iter()
                                    .map(|loc| loc.uri.to_file_path()
                                        .expect("Failed to convert URL to file path"))
                                    .collect();

                                pretty_assertions::assert_eq!(
                                    target_paths,
                                    expected_paths,
                                    "Definition locations point to unexpected schema paths\nExpected: {:?}\nActual: {:?}",
                                    expected_paths,
                                    target_paths
                                );
                            }
                        }
                    },
                    None => {
                        if !expected_paths.is_empty() {
                            panic!("No definition link was returned, but expected paths: {:?}", expected_paths);
                        }
                    }
                }

                Ok(())
            }
        };
    }
}
