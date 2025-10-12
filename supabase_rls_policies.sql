-- Este script SQL configura as Políticas de Segurança a Nível de Linha (RLS)
-- para as tabelas "pastas" e "musicas_pastas" no Supabase.
--
-- Como usar:
-- 1. Copie todo o conteúdo deste arquivo.
-- 2. No seu painel do Supabase, vá para o "SQL Editor".
-- 3. Cole o conteúdo e clique em "RUN".

-- Habilita a RLS para a tabela de pastas.
ALTER TABLE public.pastas ENABLE ROW LEVEL SECURITY;

-- Política única para a tabela "pastas":
-- Permite que os usuários realizem todas as ações (SELECT, INSERT, UPDATE, DELETE)
-- apenas nas suas próprias pastas, identificadas pelo user_id.
CREATE POLICY "Permitir gerenciamento total de pastas para donos"
ON public.pastas FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Habilita a RLS para a tabela de associação (musicas_pastas).
ALTER TABLE public.musicas_pastas ENABLE ROW LEVEL SECURITY;

-- Política única para a tabela "musicas_pastas":
-- Permite que os usuários gerenciem as músicas (adicionar, ver, remover)
-- apenas dentro das pastas que lhes pertencem. A verificação é feita
-- consultando a tabela "pastas" para encontrar o dono.
CREATE POLICY "Permitir gerenciamento de musicas em pastas para donos"
ON public.musicas_pastas FOR ALL
USING ( (SELECT user_id FROM public.pastas WHERE id = pasta_id) = auth.uid() )
WITH CHECK ( (SELECT user_id FROM public.pastas WHERE id = pasta_id) = auth.uid() );
