-- ====================================================================
--      SCRIPT DE ATUALIZAÇÃO PARA DESVINCULAR MÚSICAS SALVAS
-- ====================================================================
--
-- O que este script faz:
-- 1. Cria uma nova tabela `musicas_salvas_usuario` para armazenar
--    cópias dos dados das músicas que os usuários salvam.
-- 2. Aplica as políticas de segurança (RLS) para garantir que
--    cada usuário só possa acessar suas próprias músicas salvas.
-- 3. Fornece um comando para, opcionalmente, remover a tabela
--    antiga `musicas_pastas` depois da migração.
--
-- ====================================================================

-- PASSO 1: CRIAR A NOVA TABELA PARA MÚSICAS SALVAS

-- Esta tabela irá guardar uma "fotografia" dos dados da música no momento
-- em que ela é salva, garantindo que alterações na tabela "Musicas"
-- principal não afetem as coleções dos usuários.
CREATE TABLE IF NOT EXISTS public.musicas_salvas_usuario (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pasta_id UUID REFERENCES public.pastas(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  -- Colunas para armazenar os dados da música
  musica_titulo TEXT,
  musica_artista TEXT,
  musica_album TEXT,
  musica_url TEXT, -- O link para o áudio
  imagem_url TEXT, -- O link para a imagem da capa
  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT now()
);


-- PASSO 2: APLICAR AS POLÍTICAS DE SEGURANÇA (RLS)

-- Habilita a RLS na nova tabela.
ALTER TABLE public.musicas_salvas_usuario ENABLE ROW LEVEL SECURITY;

-- Remove a política antiga se ela já existir, para evitar erro.
DROP POLICY IF EXISTS "Permitir gerenciamento total de musicas salvas para donos" ON public.musicas_salvas_usuario;

-- Política para a tabela "musicas_salvas_usuario":
-- Garante que um usuário só pode ver, adicionar, editar ou apagar
-- as músicas que ele mesmo salvou.
CREATE POLICY "Permitir gerenciamento total de musicas salvas para donos"
ON public.musicas_salvas_usuario FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);


-- PASSO 3: LIMPEZA OPCIONAL (EXECUTAR DEPOIS DA MIGRAÇÃO)
--
-- Depois que o código da aplicação for atualizado para usar a nova
-- tabela, a tabela `musicas_pastas` não será mais necessária.
-- Você pode usar o comando abaixo para removê-la e limpar o banco.
--
-- CUIDADO: Faça um backup antes de executar este comando.
--
-- DROP TABLE IF EXISTS public.musicas_pastas;
