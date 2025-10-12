-- ====================================================================
--      SCRIPT ÚNICO PARA CONFIGURAÇÃO DE PASTAS NO SUPABASE
-- ====================================================================
--
-- Instruções:
-- 1. Copie TODO o conteúdo deste arquivo.
-- 2. No seu painel do Supabase, vá para o "SQL Editor".
-- 3. Cole o conteúdo e clique em "RUN".
--
-- O que este script faz:
-- 1. Cria a tabela `pastas` para armazenar as pastas dos usuários.
-- 2. Cria a tabela `musicas_pastas` para associar músicas às pastas.
-- 3. Habilita a Segurança a Nível de Linha (RLS) para ambas as tabelas.
-- 4. Cria as políticas que garantem que os usuários só possam
--    acessar e modificar suas próprias pastas e músicas.
--
-- ====================================================================

-- PASSO 1: CRIAR AS TABELAS

-- Tabela para armazenar as pastas criadas pelos usuários
CREATE TABLE public.pastas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  icon_class TEXT,
  bg_color TEXT,
  icon_color TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Tabela de associação para ligar músicas a pastas (relação muitos-para-muitos)
CREATE TABLE public.musicas_pastas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pasta_id UUID REFERENCES public.pastas(id) ON DELETE CASCADE,
  musica_id BIGINT REFERENCES public."Musicas"(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  -- Garante que a mesma música não possa ser adicionada duas vezes na mesma pasta
  UNIQUE(pasta_id, musica_id)
);


-- PASSO 2: APLICAR AS POLÍTICAS DE SEGURANÇA (RLS)

-- Habilita a RLS para a tabela de pastas.
ALTER TABLE public.pastas ENABLE ROW LEVEL SECURITY;

-- Política para a tabela "pastas":
-- Permite que os usuários realizem todas as ações (SELECT, INSERT, UPDATE, DELETE)
-- apenas nas suas próprias pastas.
CREATE POLICY "Permitir gerenciamento total de pastas para donos"
ON public.pastas FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Habilita a RLS para a tabela de associação (musicas_pastas).
ALTER TABLE public.musicas_pastas ENABLE ROW LEVEL SECURITY;

-- Política para a tabela "musicas_pastas":
-- Permite que os usuários gerenciem as músicas (adicionar, ver, remover)
-- apenas dentro das pastas que lhes pertencem.
CREATE POLICY "Permitir gerenciamento de musicas em pastas para donos"
ON public.musicas_pastas FOR ALL
USING ( (SELECT user_id FROM public.pastas WHERE id = pasta_id) = auth.uid() )
WITH CHECK ( (SELECT user_id FROM public.pastas WHERE id = pasta_id) = auth.uid() );
