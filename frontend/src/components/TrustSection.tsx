import { motion } from "framer-motion";
import { FeatureCard } from "@/components/ui/FeatureCard";
import { TrendingUp, Shield, BarChart3, Heart } from "lucide-react";

const drivers = [
  {
    icon: TrendingUp,
    title: "Predictive Accuracy",
    description:
      "Our ML models analyze over 40 variables to predict BP trends with 89% accuracy 7 days ahead.",
  },
  {
    icon: Shield,
    title: "Privacy-First Architecture",
    description:
      "End-to-end encryption with local-first processing. Your data never leaves your device unencrypted.",
  },
  {
    icon: BarChart3,
    title: "Explainable AI",
    description:
      "Every prediction comes with clear reasoning—understand exactly why your BP behaves the way it does.",
  },
  {
    icon: Heart,
    title: "Lifestyle Integration",
    description:
      "Connects with sleep, activity, and nutrition data to build a complete picture of your cardiovascular health.",
  },
];

const TrustSection = () => {
  return (
    <section className="section-padding relative overflow-hidden">
      {/* Background elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="gradient-blob gradient-blob-primary w-[500px] h-[500px] top-20 -right-60 opacity-10" />
        <div className="gradient-blob gradient-blob-accent w-[400px] h-[400px] -bottom-40 -left-40 opacity-10" />
      </div>

      <div className="container-clinical relative z-10">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <span className="text-glow font-display text-sm font-semibold uppercase tracking-widest mb-4 block">
            Why It Works
          </span>
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6">
            Top Drivers of Your{" "}
            <span className="text-glow">Digital Twin</span>
          </h2>
          <p className="text-muted-foreground text-lg leading-relaxed">
            Built on clinical research and validated by real outcomes. Here's what
            makes Greens Health different.
          </p>
        </motion.div>

        {/* Feature cards grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {drivers.map((driver, index) => (
            <FeatureCard
              key={driver.title}
              icon={driver.icon}
              title={driver.title}
              description={driver.description}
              index={index}
            />
          ))}
        </div>

        {/* Trust badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4, ease: [0.22, 1, 0.36, 1] }}
          className="mt-16 text-center"
        >
          <div className="inline-flex items-center gap-4 px-6 py-4 rounded-2xl bg-surface border border-border">
            <div className="w-12 h-12 rounded-xl bg-primary/50 flex items-center justify-center">
              <Shield className="w-6 h-6 text-glow" />
            </div>
            <div className="text-left">
              <p className="font-display font-semibold text-foreground">
                Clinically Validated
              </p>
              <p className="text-sm text-muted-foreground">
                Reviewed by board-certified cardiologists
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export { TrustSection };
