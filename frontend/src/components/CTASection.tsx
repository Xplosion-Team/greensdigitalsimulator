import { motion } from "framer-motion";
import { ClinicalButton } from "@/components/ui/ClinicalButton";
import { ArrowRight, Sparkles } from "lucide-react";

const CTASection = () => {
  return (
    <section className="section-padding relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-surface via-background to-background" />

      {/* Gradient blobs */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="gradient-blob gradient-blob-primary w-[700px] h-[700px] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-20" />
      </div>

      <div className="container-clinical relative z-10">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
          className="clinical-card text-center max-w-4xl mx-auto py-12 md:py-16 lg:py-20 border-glow/20 shadow-glow-sm"
        >
          {/* Icon */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
            className="w-16 h-16 mx-auto mb-8 rounded-2xl bg-cta/30 border border-glow/30 flex items-center justify-center shadow-glow-sm"
          >
            <Sparkles className="w-8 h-8 text-glow" />
          </motion.div>

          {/* Heading */}
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6"
          >
            Ready to take control of your{" "}
            <span className="text-glow text-glow">blood pressure</span>?
          </motion.h2>

          {/* Description */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4, ease: [0.22, 1, 0.36, 1] }}
            className="text-muted-foreground text-lg max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Join thousands of users who have transformed their cardiovascular health
            with personalized insights and predictive guidance.
          </motion.p>

          {/* CTA buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <ClinicalButton variant="glow" size="xl" className="group">
              Get started free
              <ArrowRight className="w-5 h-5 transition-transform duration-hover group-hover:translate-x-1" />
            </ClinicalButton>
            <ClinicalButton variant="ghost" size="lg">
              Talk to our team
            </ClinicalButton>
          </motion.div>

          {/* Fine print */}
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.6, ease: [0.22, 1, 0.36, 1] }}
            className="mt-8 text-sm text-muted-foreground/70"
          >
            No credit card required · Cancel anytime · 14-day free trial
          </motion.p>
        </motion.div>
      </div>
    </section>
  );
};

export { CTASection };
