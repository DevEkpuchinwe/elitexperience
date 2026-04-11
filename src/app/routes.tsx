import { createBrowserRouter } from "react-router";
import { CelebPage } from "./pages/CelebPage";
import { BookingPage } from "./pages/BookingPage";
import { AdminDashboard } from "./pages/AdminDashboard";
import { DefaultPage } from "./pages/DefaultPage";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: DefaultPage,
  },
  {
    path: "/:celebName",
    Component: CelebPage,
  },
  {
    path: "/:celebName/book",
    Component: BookingPage,
  },
  {
    path: "/admin",
    Component: AdminDashboard,
  },
]);
