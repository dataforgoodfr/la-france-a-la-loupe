import { clsx } from "clsx";
import type { HTMLAttributes } from "react";
import styles from "./tag.module.css";

export type TagSentiment =
  | "primary"
  | "success"
  | "warning"
  | "error"
  | "neutral"
  | "blue"
  | "shell";

export interface TagProps extends HTMLAttributes<HTMLSpanElement> {
  sentiment?: TagSentiment;
}

/**
 * Étiquette non interactive servant à catégoriser ou qualifier un contenu.
 * Un pictogramme optionnel peut être passé en enfant `svg`, avant ou après le libellé.
 */
export function Tag({ sentiment = "primary", children, className, ...htmlProps }: TagProps) {
  return (
    <span
      className={clsx(styles.tag, styles[`tag_sentiment_${sentiment}`], className)}
      {...htmlProps}
    >
      {children}
    </span>
  );
}
