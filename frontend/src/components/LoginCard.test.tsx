import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import LoginCard from "./LoginCard";

function mockFetchOnce(body: unknown, ok = true) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok,
      json: () => Promise.resolve(body),
    })
  );
}

describe("LoginCard", () => {
  beforeEach(() => {
    document.cookie = "csrftoken=test-token";
    vi.unstubAllGlobals();
  });

  it("renders the sign in form", () => {
    render(<LoginCard />);
    expect(screen.getByRole("heading", { name: /sign in/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /sign in/i })).toBeInTheDocument();
  });

  it("sends the csrf token and redirects on a successful login", async () => {
    mockFetchOnce({ ok: true, redirect: "/dashboard/" });
    delete (window as unknown as { location?: unknown }).location;
    window.location = { href: "" } as Location;

    const user = userEvent.setup();
    render(<LoginCard />);

    await user.type(screen.getByLabelText(/email address/i), "owner");
    await user.type(screen.getByLabelText(/^password$/i), "correct-horse");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => expect(window.location.href).toBe("/dashboard/"));

    const [, options] = (fetch as ReturnType<typeof vi.fn>).mock.calls[0];
    expect(options.headers["X-CSRFToken"]).toBe("test-token");
    expect(JSON.parse(options.body)).toEqual({ username: "owner", password: "correct-horse" });
  });

  it("shows the server error message when login fails", async () => {
    mockFetchOnce({ ok: false, error: "Invalid username or password." }, false);

    const user = userEvent.setup();
    render(<LoginCard />);

    await user.type(screen.getByLabelText(/email address/i), "owner");
    await user.type(screen.getByLabelText(/^password$/i), "wrong-password");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText("Invalid username or password.")).toBeInTheDocument();
  });

  it("disables the submit button while the request is in flight", async () => {
    let resolveFetch: (value: unknown) => void = () => {};
    vi.stubGlobal(
      "fetch",
      vi.fn().mockReturnValue(new Promise((resolve) => (resolveFetch = resolve)))
    );

    const user = userEvent.setup();
    render(<LoginCard />);

    await user.type(screen.getByLabelText(/email address/i), "owner");
    await user.type(screen.getByLabelText(/^password$/i), "whatever");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(screen.getByRole("button", { name: /signing in/i })).toBeDisabled();

    resolveFetch({ ok: true, json: () => Promise.resolve({ ok: false, error: "nope" }) });
    await waitFor(() =>
      expect(screen.getByRole("button", { name: /^sign in$/i })).not.toBeDisabled()
    );
  });

  it("toggles the password field between hidden and visible", async () => {
    const user = userEvent.setup();
    render(<LoginCard />);

    const passwordInput = screen.getByLabelText(/^password$/i);
    expect(passwordInput).toHaveAttribute("type", "password");

    await user.click(screen.getByRole("button", { name: /show password/i }));
    expect(passwordInput).toHaveAttribute("type", "text");

    await user.click(screen.getByRole("button", { name: /hide password/i }));
    expect(passwordInput).toHaveAttribute("type", "password");
  });
});
