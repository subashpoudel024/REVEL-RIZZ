# Use an official Python image
FROM python:3.12-slim

# Create a non-root user with UID 1000
RUN useradd -m -u 1000 user

# Create a data/cache directory with open permissions
RUN mkdir -p /data/.cache/huggingface && \
    chown -R user:user /data && \
    chmod -R 777 /data

# Set environment variables for Hugging Face cache
ENV HF_HOME=/data/.cache/huggingface \
    TRANSFORMERS_CACHE=/data/.cache/huggingface/transformers \
    HF_DATASETS_CACHE=/data/.cache/huggingface/datasets

# Switch to the non-root user
USER user

# Set working directory for the user
WORKDIR /home/user/app

# Ensure pip packages go to user space
ENV PATH=/home/user/.local/bin:$PATH

# Upgrade pip (runs as user)
RUN pip install --no-cache-dir --upgrade pip

# Copy code into the container, set ownership
COPY --chown=user . .

# Install dependencies (will go to ~/.local)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]