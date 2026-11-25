import { clsx } from "clsx";
import type { ButtonHTMLAttributes } from "react";
import styles from "./button.module.css";

export type ButtonVariant = "fill" | "outline" | "link";
export type ButtonSentiment = "primary" | "success" | "danger" | "warning" | "error" | "neutral";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  sentiment?: ButtonSentiment;

  "data-hover"?: boolean;
  "data-active"?: boolean;
  "data-focused"?: boolean;
  "data-focus-visible"?: boolean;
}

export function Button({
  variant = "fill",
  sentiment = "primary",
  children,
  type = "button",
  onClick,
  disabled,
  className,
  ...htmlProps
}: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      data-disabled={disabled}
      className={clsx(
        styles.btn,
        styles[`btn_variant_${variant}`],
        styles[`btn_sentiment_${sentiment}`],
        className,
      )}
      {...htmlProps}
    >
      {children}
    </button>
  );
}
