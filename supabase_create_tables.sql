-- PASSO 1: Criar as tabelas
-- Execute este script ANTES de aplicar as políticas de segurança (RLS).
--
-- Como usar:
-- 1. Copie todo o conteúdo deste arquivo.
-- 2. No seu painel do Supabase, vá para o "SQL Editor".
-- 3. Cole o conteúdo e clique em "RUN".

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
