import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createHashRouter, RouterProvider } from 'react-router-dom'
import { HelmetProvider } from 'react-helmet-async'
import { initializeIcons } from '@fluentui/react';

import './index.css'

import LayoutWrapper from './components/layout/LayoutWrapper.tsx'
import Chat from './pages/chat/Chat.tsx'

initializeIcons();

const routes = createHashRouter([
  {
    path: '/',
    element: <LayoutWrapper />,
    children: [
      {
        index: true,
        element: <Chat />
      },
      {
        path: 'qa',
        lazy: () => import('./pages/ask/Ask'),
      },
      {
        path: '*',
        lazy: () => import('./pages/no-page/NoPage'),
      }
    ]
  }
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <HelmetProvider>
      <RouterProvider router={routes} />
    </HelmetProvider>
  </StrictMode>,
);
