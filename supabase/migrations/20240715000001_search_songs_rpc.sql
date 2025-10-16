CREATE OR REPLACE FUNCTION search_songs(search_term TEXT)
RETURNS SETOF "Musicas" AS $$
DECLARE
    search_words TEXT[];
    word TEXT;
    query TEXT;
BEGIN
    -- Dividir o termo de busca em palavras e remover itens vazios
    search_words := array_remove(string_to_array(search_term, ' '), '');

    -- Construir a consulta base
    query := 'SELECT * FROM "Musicas" WHERE ';

    -- Adicionar uma condição para cada palavra da busca
    FOR i IN 1..array_length(search_words, 1)
    LOOP
        word := search_words[i];
        -- Adicionar AND entre as condições, exceto para a primeira
        IF i > 1 THEN
            query := query || ' AND ';
        END IF;
        -- Adicionar a condição OR para cada palavra nos três campos
        query := query || format(
            '(
                "Nome - Musica" ILIKE %L OR
                "Nome - Artista" ILIKE %L OR
                "Nome - Album" ILIKE %L
            )',
            '%' || word || '%', '%' || word || '%', '%' || word || '%'
        );
    END LOOP;

    -- Adicionar um limite para evitar consultas muito grandes
    query := query || ' LIMIT 100';

    -- Executar a consulta dinâmica
    RETURN QUERY EXECUTE query;
END;
$$ LANGUAGE plpgsql;