# Conference Abstract

**Title:** Efficient Training of Large Language Models Using Adaptive Batch Sizing

**Authors:** Dr. James Park¹, Dr. Sofia Martinez², Dr. Raj Patel¹

**Affiliations:**
1. MIT Computer Science and AI Lab
2. Google DeepMind

**Conference:** NeurIPS 2024
**Track:** Optimization Methods
**Submission Date:** October 1, 2024

---

## Abstract

We propose AdaptiveBatch, a novel training algorithm that dynamically adjusts batch sizes based on gradient variance and computational efficiency. Traditional fixed-batch training suffers from suboptimal resource utilization and convergence issues when scaling to models with 100B+ parameters.

Our method monitors gradient signal quality in real-time and automatically scales batch size between 512 and 8192 samples per step. On GPT-3 scale models, we demonstrate:

- 35% reduction in training time
- 22% improvement in final perplexity
- Better GPU utilization (avg 92% vs 78%)
- Reduced memory fragmentation

We evaluate AdaptiveBatch on three domains: language modeling (1B-175B parameters), image classification (ViT-Giant), and multi-modal learning (CLIP-scale). Results show consistent improvements across all settings.

**Keywords:** deep learning, optimization, large language models, distributed training, efficiency

**Code:** Available at github.com/mlresearch/adaptivebatch

---

**Presentation Preference:** Oral + Poster
**Contact:** james.park@mit.edu

