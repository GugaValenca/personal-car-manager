import { useEffect, useMemo, useState } from "react";
import { Car, DollarSign, Fuel, Route } from "lucide-react";
import carBg from "@/assets/car-bg.jpg";
import LoginCard from "@/components/LoginCard";

type DashboardResponse = {
  summary: {
    total_cars: number;
    total_expenses: number;
    total_maintenance_cost: number;
    total_fuel_cost: number;
    total_trip_income: number;
    total_trip_distance: number;
    net_balance: number;
  };
};

const API_URL = "/api/dashboard/";

const money = (value: number) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);

const Index = () => {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const response = await fetch(API_URL, {
          credentials: "include",
          headers: { Accept: "application/json" },
        });
        if (!response.ok) {
          throw new Error("unauthorized");
        }
        const body = (await response.json()) as DashboardResponse;
        setData(body);
      } catch {
        setData(null);
      } finally {
        setLoading(false);
      }
    };
    loadSummary();
  }, []);

  const cards = useMemo(() => {
    if (!data) return [];
    return [
      {
        icon: Car,
        label: "Vehicles",
        value: data.summary.total_cars.toString(),
      },
      {
        icon: DollarSign,
        label: "Net Balance",
        value: money(data.summary.net_balance),
      },
      {
        icon: Fuel,
        label: "Fuel Cost",
        value: money(data.summary.total_fuel_cost),
      },
      {
        icon: Route,
        label: "Trip Distance",
        value: `${data.summary.total_trip_distance} km`,
      },
    ];
  }, [data]);

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${carBg})` }}
      />
      <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/75 to-background/65" />
      <div className="relative z-10 flex min-h-screen flex-col">
        <header className="flex items-center justify-between px-6 py-5 md:px-12">
          <div className="flex items-center gap-2.5 animate-fade-in-up">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/15 border border-primary/20">
              <Car className="h-5 w-5 text-primary" />
            </div>
            <span className="text-sm font-semibold tracking-wider text-foreground/90 uppercase">
              Personal Car Manager Hub
            </span>
          </div>
          <a
            href="/admin/"
            className="rounded-md border border-primary/25 bg-primary/10 px-3 py-1.5 text-xs font-medium text-primary"
          >
            Admin Access
          </a>
        </header>

        <main className="flex flex-1 flex-col lg:flex-row items-center px-6 md:px-12 lg:px-20 pb-8 gap-8 lg:gap-16">
          <section className="flex flex-1 flex-col justify-center max-w-xl lg:max-w-lg py-8 lg:py-0">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.25em] text-primary">
              Personal, Taxi and Fleet Control
            </p>
            <h1 className="text-4xl md:text-5xl lg:text-[3.2rem] font-semibold leading-tight text-foreground mb-5">
              Full car cost management with
              <span className="text-primary"> real operation metrics</span>.
            </h1>
            <p className="text-base md:text-lg leading-relaxed text-muted-foreground mb-8 max-w-md">
              Use this frontend with Django APIs to monitor maintenance, expenses, fuel records,
              trips, and profitability for personal cars or fleets.
            </p>

            {loading ? (
              <p className="text-sm text-muted-foreground">Loading operation summary...</p>
            ) : data ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {cards.map((card) => (
                  <div
                    key={card.label}
                    className="rounded-xl border border-border/60 bg-secondary/40 px-4 py-3"
                  >
                    <div className="mb-1 flex items-center gap-2 text-xs text-muted-foreground">
                      <card.icon className="h-3.5 w-3.5 text-primary" />
                      {card.label}
                    </div>
                    <p className="text-lg font-semibold text-foreground">{card.value}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                Sign in via admin to load live dashboard data from <code>/api/dashboard/</code>.
              </p>
            )}
          </section>

          <section className="w-full max-w-md lg:max-w-[420px] animate-fade-in-up animate-delay-200">
            <LoginCard />
          </section>
        </main>
      </div>
    </div>
  );
};

export default Index;
