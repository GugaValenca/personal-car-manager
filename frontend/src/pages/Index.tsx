import { Car, Shield, Gauge } from "lucide-react";
import carBg from "@/assets/car-bg.jpg";
import LoginCard from "@/components/LoginCard";

const Index = () => {
  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${carBg})` }}
      />
      <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/70 to-background/50" />
      <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-background/40" />

      <div className="relative z-10 flex min-h-screen flex-col">
        <header className="flex items-center justify-between px-6 py-5 md:px-12">
          <div className="flex items-center gap-2.5 animate-fade-in-up">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/15 border border-primary/20">
              <Car className="h-5 w-5 text-primary" />
            </div>
            <span
              className="text-sm font-semibold tracking-wider text-foreground/90 uppercase"
              style={{ fontFamily: "Inter, sans-serif" }}
            >
              PERSONAL CAR MANAGER
            </span>
          </div>
          <a
            href="/admin/"
            className="rounded-md border border-primary/25 bg-primary/10 px-3 py-1.5 text-xs font-medium text-primary"
            style={{ fontFamily: "Inter, sans-serif" }}
          >
            Admin Access
          </a>
        </header>

        <main className="flex flex-1 flex-col lg:flex-row items-center px-6 md:px-12 lg:px-20 pb-8 gap-8 lg:gap-16">
          <section className="flex flex-1 flex-col justify-center max-w-xl lg:max-w-lg py-8 lg:py-0">
            <div className="animate-fade-in-left animate-delay-100">
              <p
                className="mb-4 text-xs font-semibold uppercase tracking-[0.25em] text-primary"
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                Personal Car Manager
              </p>
            </div>

            <h1 className="animate-fade-in-left animate-delay-200 text-4xl md:text-5xl lg:text-[3.4rem] font-semibold leading-tight text-foreground mb-6">
              Your vehicles, <span className="text-primary">organized</span> in one
              place.
            </h1>

            <p
              className="animate-fade-in-left animate-delay-300 text-base md:text-lg leading-relaxed text-muted-foreground mb-10 max-w-md"
              style={{ fontFamily: "Inter, sans-serif" }}
            >
              Track maintenance, monitor expenses, and manage your entire fleet
              with a practical dashboard built for everyday car ownership.
            </p>

            <div
              className="animate-fade-in-left animate-delay-400 flex flex-wrap gap-3"
              style={{ fontFamily: "Inter, sans-serif" }}
            >
              {[
                { icon: Car, label: "Vehicle Registry" },
                { icon: Shield, label: "Maintenance Logs" },
                { icon: Gauge, label: "Expense Tracking" },
              ].map(({ icon: Icon, label }) => (
                <div
                  key={label}
                  className="flex items-center gap-2 rounded-full border border-border/60 bg-secondary/40 px-4 py-2 text-xs font-medium text-secondary-foreground"
                >
                  <Icon className="h-3.5 w-3.5 text-primary" />
                  {label}
                </div>
              ))}
            </div>
          </section>

          <section className="w-full max-w-md lg:max-w-[420px] animate-fade-in-up animate-delay-200">
            <LoginCard />
          </section>
        </main>

        <footer className="px-6 py-4 md:px-12 animate-fade-in-up animate-delay-500">
          <p
            className="text-[11px] text-muted-foreground/50 text-center lg:text-left"
            style={{ fontFamily: "Inter, sans-serif" }}
          >
            © 2026 Personal Car Manager — A fullstack portfolio project
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
