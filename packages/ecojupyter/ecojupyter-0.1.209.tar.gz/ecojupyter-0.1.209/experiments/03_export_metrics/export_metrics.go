// Description: This program exports power consumption metrics from JupyterHub singleuser pods
// to CSV files. It uses the Prometheus API to query the metrics and Kubernetes client-go
// to list the pods. The program takes a namespace and output directory as command-line arguments.
// It requires the PROM_URL environment variable to be set to the Prometheus endpoint.

package main

import (
	"context"
	"encoding/csv"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	// "strconv"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"

	"github.com/prometheus/client_golang/api"
	promapiv1 "github.com/prometheus/client_golang/api/prometheus/v1"
	"github.com/prometheus/common/model"
)

func main() {
	// CLI flags
	namespace := flag.String("namespace", "jhub", "Kubernetes namespace where JupyterHub runs")
	outputDir := flag.String("output-dir", "./metrics", "Directory to write CSV files into")
	flag.Parse()

	// Prometheus URL from environment
	promURL := os.Getenv("PROM_URL")
	if promURL == "" {
		log.Fatal("Please set PROM_URL environment variable to your Prometheus endpoint, e.g. http://localhost:9090")
	}

	// Kubernetes client config
	config, err := rest.InClusterConfig()
	if err != nil {
		// fallback to kubeconfig
		kubeconfig := filepath.Join(os.Getenv("HOME"), ".kube", "config")
		config, err = clientcmd.BuildConfigFromFlags("", kubeconfig)
		if err != nil {
			log.Fatalf("Failed to load Kubernetes config: %v", err)
		}
	}
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		log.Fatalf("Failed to create Kubernetes client: %v", err)
	}

	// Prometheus client
	promClient, err := api.NewClient(api.Config{Address: promURL})
	if err != nil {
		log.Fatalf("Error creating Prometheus client: %v", err)
	}
	promAPI := promapiv1.NewAPI(promClient)

	// Ensure output directory
	err = os.MkdirAll(*outputDir, 0755)
	if err != nil {
		log.Fatalf("Error creating output directory: %v", err)
	}

	// List singleuser pods
	podList, err := clientset.CoreV1().Pods(*namespace).List(context.Background(), metav1.ListOptions{
		LabelSelector: "component=singleuser-server",
	})
	if err != nil {
		log.Fatalf("Failed to list pods: %v", err)
	}

	// Process each pod
	for _, pod := range podList.Items {
		name := pod.Name
		start := pod.CreationTimestamp.Time
		end := time.Now().UTC()
		if pod.DeletionTimestamp != nil {
			end = pod.DeletionTimestamp.Time
		}

		log.Printf("Exporting metrics for pod %s (from %s to %s)", name, start, end)

		// Build PromQL query
		query := fmt.Sprintf("scaph_process_power_consumption_microwatts{pod=\"%s\"}", name)
		time_range := promapiv1.Range{Start: start, End: end, Step: time.Duration(15) * time.Second}

		matrixResult, warnings, err := promAPI.QueryRange(context.Background(), query, time_range)
		if err != nil {
			log.Printf("QueryRange failed for pod %s: %v", name, err)
			continue
		}
		if len(warnings) > 0 {
			log.Printf("Warnings for pod %s: %v", name, warnings)
		}

		matrix, ok := matrixResult.(model.Matrix)
		if !ok || len(matrix) == 0 {
			log.Printf("No data for pod %s", name)
			continue
		}

		// Write CSV
		csvFile := filepath.Join(*outputDir, name+".csv")
		f, err := os.Create(csvFile)
		if err != nil {
			log.Printf("Failed to create CSV for %s: %v", name, err)
			continue
		}
		writer := csv.NewWriter(f)
		_ = writer.Write([]string{"timestamp", "value_microwatts"})

		// Assume first time series
		for _, sample := range matrix[0].Values {
			t := sample.Timestamp.Time().UTC().Format(time.RFC3339)
			val := fmt.Sprintf("%f", float64(sample.Value))
			_ = writer.Write([]string{t, val})
		}

		writer.Flush()
		f.Close()
		log.Printf("Wrote %s", csvFile)
	}
}
