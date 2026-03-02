import { useState } from "react";
import { Eye, EyeOff, LogIn } from "lucide-react";

const LoginCard = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (!response.ok || !data.ok) {
        throw new Error(data.error || "Invalid credentials.");
      }

      window.location.href = data.redirect || "/dashboard/";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card p-8 md:p-10">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-foreground mb-1.5">Sign In</h2>
        <p className="text-sm text-muted-foreground" style={{ fontFamily: "Inter, sans-serif" }}>
          Access your vehicle dashboard
        </p>
      </div>

      {error ? (
        <div className="mb-4 rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive-foreground">
          {error}
        </div>
      ) : null}

      <form onSubmit={handleSubmit} className="space-y-5" style={{ fontFamily: "Inter, sans-serif" }}>
        <div>
          <label htmlFor="email" className="mb-1.5 block text-xs font-medium text-secondary-foreground">
            Email Address
          </label>
          <input
            id="email"
            type="text"
            placeholder="you@example.com"
            className="input-glass"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="password" className="mb-1.5 block text-xs font-medium text-secondary-foreground">
            Password
          </label>
          <div className="relative">
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              className="input-glass pr-11"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword((v) => !v)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs">
          <label className="flex items-center gap-2 cursor-pointer text-secondary-foreground">
            <input type="checkbox" className="h-3.5 w-3.5 rounded border-border accent-primary" />
            Remember me
          </label>
          <a href="/admin/password_reset/" className="text-primary hover:text-primary/80 transition-colors font-medium">
            Forgot password?
          </a>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn-primary flex items-center justify-center gap-2 mt-2 disabled:opacity-70"
        >
          <LogIn className="h-4 w-4" />
          {loading ? "Signing in..." : "Sign In"}
        </button>
      </form>

      <div className="my-6 flex items-center gap-3">
        <div className="h-px flex-1 bg-border/40" />
        <span
          className="text-[11px] text-muted-foreground/60 uppercase tracking-wider"
          style={{ fontFamily: "Inter, sans-serif" }}
        >
          or
        </span>
        <div className="h-px flex-1 bg-border/40" />
      </div>

      <p className="text-center text-sm text-muted-foreground" style={{ fontFamily: "Inter, sans-serif" }}>
        Don&apos;t have an account?{" "}
        <a href="/signup/" className="font-medium text-primary hover:text-primary/80 transition-colors">
          Create one
        </a>
      </p>
    </div>
  );
};

export default LoginCard;
