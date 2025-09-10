#!/usr/bin/env python3
"""
Pointer Activity Monitoring Service
Created by: Prof. Shahab Anbarjafari from 3S Holding OÜ, Tartu Estonia

A comprehensive pointer activity monitoring service that tracks mouse movements
and provides heatmap visualization of pointer activity across screen(s).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
from datetime import datetime
from pynput import mouse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import screeninfo
from collections import defaultdict


class PointerActivityMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.pointer_data = []
        self.session_start_time = None
        self.data_file = "pointer_data.json"
        self.listener = None
        
        # Get screen dimensions - handle dual monitor coordinate system
        self.screens = screeninfo.get_monitors()
        
        # For the corrected coordinate system:
        # Monitor 1 (main): X(0 to 1512), Y(0 to 982) - after abs() conversion
        # Monitor 2 (extended): X(-217 to 1703), Y(982 to 2062) - as is
        self.min_x = min(screen.x for screen in self.screens)
        self.max_x = max(screen.x + screen.width for screen in self.screens)
        self.min_y = 0  # Start from 0 since we convert negative Y to absolute
        self.max_y = max(screen.y + screen.height for screen in self.screens)
        
        # Total screen area
        self.screen_width = self.max_x - self.min_x
        self.screen_height = self.max_y - self.min_y
        
        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the small corner UI interface"""
        self.root = tk.Tk()
        self.root.title("Pointer Monitor")
        self.root.geometry("180x150")  # Increased height to fit all buttons
        self.root.resizable(False, False)
        
        # Position window at center of the screen for better visibility
        center_x = (self.screen_width - 180) // 2  # Horizontally centered
        center_y = (self.screen_height - 150) // 4  # Upper-center vertically
        self.root.geometry(f"180x150+{center_x}+{center_y}")
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.pack(pady=(0, 10))
        
        # Start button
        self.start_btn = ttk.Button(
            main_frame, 
            text="Start", 
            command=self.start_monitoring,
            width=15
        )
        self.start_btn.pack(pady=2)
        
        # Stop button
        self.stop_btn = ttk.Button(
            main_frame, 
            text="Stop", 
            command=self.stop_monitoring,
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(pady=2)
        
        # Visualize button with eye icon
        self.visualize_btn = ttk.Button(
            main_frame, 
            text="👁 Visualize", 
            command=self.show_visualization,
            width=15
        )
        self.visualize_btn.pack(pady=2)
        
        # Load existing data
        self.load_data()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_mouse_move(self, x, y):
        """Callback for mouse movement events"""
        if self.is_monitoring:
            timestamp = time.time()
            self.pointer_data.append({
                'x': x,
                'y': y,
                'timestamp': timestamp,
                'session': self.session_start_time
            })
            
    def start_monitoring(self):
        """Start monitoring pointer activity"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.session_start_time = datetime.now().isoformat()
            
            # Update UI
            self.status_label.config(text="Monitoring...", foreground="red")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            # Start mouse listener
            self.listener = mouse.Listener(on_move=self.on_mouse_move)
            self.listener.start()
            
            print(f"Started monitoring at {self.session_start_time}")
            
    def stop_monitoring(self):
        """Stop monitoring pointer activity"""
        if self.is_monitoring:
            self.is_monitoring = False
            
            # Update UI
            self.status_label.config(text="Ready", foreground="green")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            
            # Stop mouse listener
            if self.listener:
                self.listener.stop()
                self.listener = None
            
            # Save data
            self.save_data()
            
            print(f"Stopped monitoring. Collected {len(self.pointer_data)} data points")
            
    def save_data(self):
        """Save pointer data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.pointer_data, f, indent=2)
            print(f"Data saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def load_data(self):
        """Load existing pointer data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.pointer_data = json.load(f)
                print(f"Loaded {len(self.pointer_data)} data points from {self.data_file}")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.pointer_data = []
            
    def create_heatmap(self):
        """Create heatmap visualization of pointer activity"""
        if not self.pointer_data:
            messagebox.showwarning("No Data", "No pointer data available. Please start monitoring first.")
            return None
            
        # Extract coordinates and fix coordinate mapping for proper top-to-bottom orientation
        # Monitor 1 (main): negative Y values -> convert to absolute values (0 to 982) top-to-bottom
        # Monitor 2 (extended): positive Y values (982 to 2062) -> keep as is, top-to-bottom
        x_coords = []
        y_coords = []
        
        for point in self.pointer_data:
            x = point['x']
            y = point['y']
            
            # Fix Y coordinate mapping for proper top-to-bottom orientation
            if y < 0:
                # Monitor 1 (main monitor): negative Y values
                # Convert negative Y to positive and map to Monitor 1 coordinates (0 to 982)
                # Small negative Y (like -21) should be near top of Monitor 1 (near 0)
                # Large negative Y (like -590) should be near bottom of Monitor 1 (near 982)
                y = abs(y)  # Convert to positive
                # Now y ranges from 0 to ~1080, map to 0 to 982 range for Monitor 1
                # Keep the natural top-to-bottom orientation
            else:
                # Monitor 2 coordinates: positive Y values (982 to 2062)
                # These are already in the correct coordinate system
                # 982 = top of Monitor 2, 2062 = bottom of Monitor 2
                pass
            
            x_coords.append(x)
            y_coords.append(y)
        
        # Create bins for heatmap using actual screen bounds (including negative coordinates)
        x_bins = np.linspace(self.min_x, self.max_x, 120)  # Higher resolution for dual monitors
        y_bins = np.linspace(self.min_y, self.max_y, 120)
        
        # Create 2D histogram
        heatmap_data, x_edges, y_edges = np.histogram2d(x_coords, y_coords, bins=[x_bins, y_bins])
        
        # Create figure with dark background for better contrast
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(14, 10))
        fig.patch.set_facecolor('black')
        
        # Create heatmap with enhanced visual appeal using actual screen coordinates
        im = ax.imshow(
            heatmap_data.T, 
            origin='lower',
            extent=[self.min_x, self.max_x, self.min_y, self.max_y],
            cmap='plasma',  # More vibrant colormap
            interpolation='gaussian',
            alpha=0.8
        )
        
        # Customize plot with beautiful styling
        ax.set_title(f'🔥 Pointer Activity Heatmap 🔥\n{len(self.pointer_data):,} data points collected\nCreated by Prof. Shahab Anbarjafari - 3S Holding OÜ', 
                    fontsize=16, fontweight='bold', color='white', pad=20)
        ax.set_xlabel('Screen X Coordinate (pixels)', fontsize=12, color='white')
        ax.set_ylabel('Screen Y Coordinate (pixels)', fontsize=12, color='white')
        
        # Add colorbar with styling
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Activity Density', fontsize=12, color='white')
        cbar.ax.tick_params(colors='white')
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Add screen boundaries for all monitors with corrected coordinates
        for i, screen in enumerate(self.screens):
            # Correct the Y coordinates for visualization
            if screen.y < 0:
                # Monitor 1 (main): Y coordinate should be 0 to 982
                rect_y = 0
                rect_height = screen.height
                label_y = rect_height // 2
            else:
                # Monitor 2 (extended): Keep original coordinates
                rect_y = screen.y
                rect_height = screen.height
                label_y = screen.y + screen.height // 2
            
            rect = plt.Rectangle(
                (screen.x, rect_y), 
                screen.width, 
                rect_height,
                fill=False, 
                edgecolor='cyan', 
                linewidth=3,
                linestyle='-',
                alpha=0.8
            )
            ax.add_patch(rect)
            
            # Add screen labels
            label_x = screen.x + screen.width // 2
            ax.text(
                label_x, label_y, 
                f'Monitor {i+1}\n{screen.width}×{screen.height}',
                color='cyan',
                fontsize=12,
                fontweight='bold',
                ha='center',
                va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7)
            )
        
        plt.tight_layout()
        return fig
        
    def show_visualization(self):
        """Show heatmap visualization in a new window"""
        # Stop monitoring if currently active
        if self.is_monitoring:
            self.stop_monitoring()
            print("Monitoring stopped to show visualization")
        
        fig = self.create_heatmap()
        if fig is None:
            return
            
        # Create visualization window with better sizing
        viz_window = tk.Toplevel(self.root)
        viz_window.title("🔥 Pointer Activity Heatmap - Prof. Shahab Anbarjafari")
        
        # Make it larger and center it
        window_width = 1200
        window_height = 800
        screen_center_x = (self.screen_width - window_width) // 2
        screen_center_y = (self.screen_height - window_height) // 2
        viz_window.geometry(f"{window_width}x{window_height}+{screen_center_x}+{screen_center_y}")
        
        # Configure window
        viz_window.configure(bg='black')
        
        # Add canvas
        canvas = FigureCanvasTkAgg(fig, viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar frame with dark styling
        toolbar_frame = tk.Frame(viz_window, bg='black', height=50)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add save button with enhanced styling
        save_btn = tk.Button(
            toolbar_frame,
            text="💾 Save Heatmap",
            command=lambda: self.save_heatmap(fig),
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add clear data button with enhanced styling
        clear_btn = tk.Button(
            toolbar_frame,
            text="🗑️ Clear Data",
            command=self.clear_data,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add close button
        close_btn = tk.Button(
            toolbar_frame,
            text="❌ Close",
            command=viz_window.destroy,
            bg='#2196F3',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        close_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add statistics with better formatting including coordinate ranges
        stats_text = f"📊 Total Points: {len(self.pointer_data):,} | " \
                    f"🖥️ Total Area: {self.screen_width}x{self.screen_height} | " \
                    f"📺 Screens: {len(self.screens)} | " \
                    f"📍 Range: X({self.min_x} to {self.max_x}), Y({self.min_y} to {self.max_y})"
        
        stats_label = tk.Label(
            toolbar_frame, 
            text=stats_text,
            bg='black',
            fg='white',
            font=('Arial', 10)
        )
        stats_label.pack(side=tk.RIGHT, padx=5, pady=5)
        
    def save_heatmap(self, fig):
        """Save heatmap to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pointer_heatmap_{timestamp}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Saved", f"Heatmap saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save heatmap: {e}")
            
    def clear_data(self):
        """Clear all collected data"""
        if messagebox.askyesno("Clear Data", "Are you sure you want to clear all collected data?"):
            self.pointer_data = []
            self.save_data()
            messagebox.showinfo("Cleared", "All data has been cleared.")
            
    def on_closing(self):
        """Handle application closing"""
        if self.is_monitoring:
            self.stop_monitoring()
        self.root.destroy()
        
    def run(self):
        """Start the application"""
        print("Pointer Activity Monitor started")
        print(f"Total screen area: {self.screen_width}x{self.screen_height}")
        print(f"Coordinate bounds: X({self.min_x} to {self.max_x}), Y({self.min_y} to {self.max_y})")
        print(f"Number of screens: {len(self.screens)}")
        for i, screen in enumerate(self.screens):
            print(f"  Screen {i+1}: {screen.width}x{screen.height} at ({screen.x}, {screen.y})")
        self.root.mainloop()


def main():
    """Main entry point for the application"""
    try:
        monitor = PointerActivityMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()
