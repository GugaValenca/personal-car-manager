import { FormEvent, useState } from "react";
import { Eye, EyeOff, LogIn } from "lucide-react";

const LoginCard = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();

    const form = document.createElement("form");
    form.method = "POST";
    form.action = "/admin/login/?next=/dashboard/";

    const csrf = document.cookie
      .split("; ")
      .find((item) => item.startsWith("csrftoken="))
      ?.split("=")[1];

    const addInput = (name: string, value: string) => {
      const input = document.createElement("input");
      input.type = "hidden";
      input.name = name;
      input.value = value;
      form.appendChild(input);
    };

    addInput("username", username);
    addInput("password", password);
    addInput("next", "/dashboard/");
    if (csrf) addInput("csrfmiddlewaretoken", csrf);

    document.body.appendChild(form);
    form.submit();
  };

  return (
    <div className="glass-card p-8 md:p-10">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-foreground mb-1.5">Sign In</h2>
        <p className="text-sm text-muted-foreground">Access your vehicle dashboard</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="username" className="mb-1.5 block text-xs font-medium text-secondary-foreground">
            Username
          </label>
          <input
            id="username"
            type="text"
            placeholder="admin username"
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
              placeholder="********"
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

        <button type="submit" className="btn-primary flex items-center justify-center gap-2 mt-2">
          <LogIn className="h-4 w-4" />
          Sign In
        </button>
      </form>

      <div className="my-6 flex items-center gap-3">
        <div className="h-px flex-1 bg-border/40" />
        <span className="text-[11px] text-muted-foreground/60 uppercase tracking-wider">or</span>
        <div className="h-px flex-1 bg-border/40" />
      </div>

      <p className="text-center text-sm text-muted-foreground">
        Need access?{" "}
        <a href="/admin/" className="font-medium text-primary hover:text-primary/80 transition-colors">
          Open admin
        </a>
      </p>
    </div>
  );
};

export default LoginCard;
