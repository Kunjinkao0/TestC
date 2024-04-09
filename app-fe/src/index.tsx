import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.scss';

import SearchPage from './pages/Search';
import DetailPage from './pages/Detail';
import AdminPage from './pages/Admin';

const router = createBrowserRouter([
  {
    path: "/",
    element: <SearchPage />,
  },
  {
    path: "detail",
    element: <DetailPage />,
  },
  {
    path: "admin",
    element: <AdminPage />,
  },
]);

ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
).render(
  <RouterProvider router={router} />
);