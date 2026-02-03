import "./globals.css";

export const metadata = {
  title: "Movie Semantic Search",
  description: "Semantic search over movies + QA",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-zinc-50 text-zinc-900">
          {children}
        </div>
      </body>
    </html>
  );
}