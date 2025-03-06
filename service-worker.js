// Remover o Service Worker
self.addEventListener('install', (event) => {
  console.log('Service Worker instalado');
});

// Interceptar requisições e servir diretamente do servidor
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
  );
});

// Manter a música tocando com sincronização em segundo plano
self.addEventListener('message', (event) => {
  if (event.data === 'keep-alive') {
    console.log('Manter ativo no segundo plano');
  }
});
