import { motion } from "framer-motion";
import { StatCard } from "@/components/ui/StatCard";

const stats = [
  { value: 27, label: "Paying Users", suffix: "" },
  { value: 35, label: "Monthly Active Users", suffix: "" },
  { value: 3386, label: "BP Readings Logged", suffix: "" },
  { value: 51, label: "Controlled <140/90", suffix: "%" },
  { value: 4.5, label: "Avg Systolic Reduction", suffix: " mmHg" },
];

const OutcomesStrip = () => {
  return (
    <section className="relative py-16 md:py-24 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-surface to-background" />

      {/* Hairline borders */}
      <div className="absolute inset-x-0 top-0 h-px bg-border" />
      <div className="absolute inset-x-0 bottom-0 h-px bg-border" />

      <div className="container-clinical relative z-10">
        {/* Section label */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="text-center mb-12"
        >
          <span className="text-glow font-display text-sm font-semibold uppercase tracking-widest">
            Real Results
          </span>
        </motion.div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 md:gap-0 md:divide-x divide-border">
          {stats.map((stat, index) => (
            <StatCard
              key={stat.label}
              value={stat.value}
              suffix={stat.suffix}
              label={stat.label}
              duration={1500 + index * 200}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export { OutcomesStrip };
