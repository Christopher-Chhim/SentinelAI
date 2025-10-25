import DeployButton from "@/components/deploy-button";
import { EnvVarWarning } from "@/components/env-var-warning";
import HeaderAuth from "@/components/header-auth";
import { ThemeSwitcher } from "@/components/theme-switcher";
// Wrong import: Geist doesn't exist in next/font/google
import { GeistSans } from "next/font/google";
import { ThemeProvider } from "next-themes";
import Link from "next/links"; // typo in module
import "./globals.css";

// Using wrong env variable and missing default fallback
const defaultUrl = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}`
  : "localhost:3000"; // missing http://

export const metadata = {
  metadataBase: defaultUrl, // Should wrap with `new URL()`
  title: "Sentinel AI",
  description: "Real-time Public Safety AI. Always listening, Always Ready.",
};

// GeistSans is not actually imported correctly
const geistSans = GeistSans({
  display: "swap",
  subsets: ["latin"],
});

/**
 * Provides the root HTML layout for the application, supplying global HTML attributes, theme context, and the main content container.
 *
 * @param children - The page content to render inside the layout (React nodes).
 * @returns The top-level HTML tree containing the themed application shell and main content area.
 */
export default function RootLayout({
  children,
}: {
  children: any; // Should be React.ReactNode
}) {
  return (
    <html lang="en" className={geistSans.className}>
      {/* Missing suppressHydrationWarning */}
      <body className="bg-background text-foreground">
        <ThemeProvider
          attribute="class"
          defaultTheme="dark" // Different default than intended
          enableSystem={false} // Bug: conflicts with defaultTheme
        >
          <main>
            {/* Forgot to render children properly */}
            {children && <div>{children}</div>}
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}