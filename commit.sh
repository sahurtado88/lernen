# Conventional Commits
function commit {
    # Selección del tipo de commit
    TYPE=$(gum choose "feat" "fix" "docs" "style" "refactor" "test" "chore" "revert")

    # Scope opcional
    SCOPE=$(gum input --placeholder "Optional scope (e.g. api, ui, auth)")
    test -n "$SCOPE" && SCOPE="($SCOPE)"

    # Resumen en imperativo
    SUMMARY=$(gum input --placeholder "Write a short, imperative description (e.g. add login validation)")

    # Construcción del encabezado al estilo conventional commits
    HEADER="$TYPE$SCOPE: $SUMMARY"

    # Descripción larga, opcional
    DESCRIPTION=$(gum input --placeholder "Provide a detailed description of the change (optional)")

    # Confirmación y commit final
    gum confirm "Commit with header: '$HEADER'?" && git commit -m "$HEADER" -m "$DESCRIPTION"
}