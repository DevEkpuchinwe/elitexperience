import { useNavigate } from "react-router";

export function DefaultPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black flex items-center justify-center p-4">
      <div className="max-w-2xl text-center space-y-8">
        <h1 className="text-6xl text-white">
          Celebrity Access
        </h1>
        <p className="text-xl text-white/80">
          Select a celebrity to view their exclusive booking page
        </p>
        <div className="space-y-4">
          <button
            onClick={() => navigate('/taylor-swift')}
            className="w-full bg-white/10 backdrop-blur-lg border border-white/20 text-white px-8 py-6 rounded-xl hover:bg-white/20 transition-all text-xl"
          >
            View Taylor Swift
          </button>
          <button
            onClick={() => navigate('/default')}
            className="w-full bg-white/10 backdrop-blur-lg border border-white/20 text-white px-8 py-6 rounded-xl hover:bg-white/20 transition-all text-xl"
          >
            View Default Artist
          </button>
        </div>
        <p className="text-white/60 text-sm mt-8">
          You can also visit directly: yoursite.com/[celebrity-name]
        </p>
      </div>
    </div>
  );
}
