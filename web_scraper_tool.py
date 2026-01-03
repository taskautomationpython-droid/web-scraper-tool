import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime
import threading

class WebScraperTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper Tool - by Dumok Data Lab")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2c3e50', foreground='white')
        style.configure('TLabel', background='#2c3e50', foreground='white')
        style.configure('TButton', font=('Arial', 10), padding=10)
        
        self.create_widgets()
        
    def create_widgets(self):
        # 타이틀
        title_frame = tk.Frame(self.root, bg='#34495e', pady=15)
        title_frame.pack(fill='x')
        
        title = ttk.Label(title_frame, text="🌐 Web Scraper Tool", style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(title_frame, text="Extract data from any website", font=('Arial', 10))
        subtitle.pack()
        
        # 메인 컨테이너
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # URL 입력
        url_frame = tk.Frame(main_frame, bg='#2c3e50')
        url_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(url_frame, text="Target URL:").pack(anchor='w')
        
        url_input_frame = tk.Frame(url_frame, bg='#2c3e50')
        url_input_frame.pack(fill='x', pady=(5, 0))
        
        self.url_entry = tk.Entry(url_input_frame, font=('Arial', 10), bg='white', fg='black')
        self.url_entry.pack(side='left', fill='x', expand=True, ipady=8)
        self.url_entry.insert(0, "https://example.com")
        
        # 선택자 입력
        selector_frame = tk.Frame(main_frame, bg='#2c3e50')
        selector_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(selector_frame, text="CSS Selector (e.g., 'h1', '.class', '#id'):").pack(anchor='w')
        
        self.selector_entry = tk.Entry(selector_frame, font=('Arial', 10), bg='white', fg='black')
        self.selector_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.selector_entry.insert(0, "h1")
        
        # 옵션
        options_frame = tk.Frame(main_frame, bg='#2c3e50')
        options_frame.pack(fill='x', pady=(0, 15))
        
        self.extract_text_var = tk.BooleanVar(value=True)
        self.extract_links_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(options_frame, text="Extract Text", variable=self.extract_text_var, 
                      bg='#2c3e50', fg='white', selectcolor='#34495e', 
                      font=('Arial', 10)).pack(side='left', padx=(0, 20))
        
        tk.Checkbutton(options_frame, text="Extract Links", variable=self.extract_links_var,
                      bg='#2c3e50', fg='white', selectcolor='#34495e',
                      font=('Arial', 10)).pack(side='left')
        
        # 버튼
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill='x', pady=(0, 15))
        
        self.scrape_btn = tk.Button(button_frame, text="🚀 Start Scraping", 
                                    command=self.start_scraping,
                                    bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                                    relief='flat', padx=20, pady=10, cursor='hand2')
        self.scrape_btn.pack(side='left', padx=(0, 10))
        
        self.export_csv_btn = tk.Button(button_frame, text="💾 Export CSV",
                                       command=self.export_csv,
                                       bg='#3498db', fg='white', font=('Arial', 10),
                                       relief='flat', padx=15, pady=10, cursor='hand2',
                                       state='disabled')
        self.export_csv_btn.pack(side='left', padx=(0, 10))
        
        self.export_json_btn = tk.Button(button_frame, text="📄 Export JSON",
                                        command=self.export_json,
                                        bg='#9b59b6', fg='white', font=('Arial', 10),
                                        relief='flat', padx=15, pady=10, cursor='hand2',
                                        state='disabled')
        self.export_json_btn.pack(side='left')
        
        # 결과 표시
        result_label = ttk.Label(main_frame, text="Results:")
        result_label.pack(anchor='w', pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(main_frame, width=80, height=20,
                                                     font=('Consolas', 9),
                                                     bg='#ecf0f1', fg='#2c3e50',
                                                     relief='flat')
        self.result_text.pack(fill='both', expand=True)
        
        # 상태바
        self.status_label = ttk.Label(self.root, text="Ready", 
                                     font=('Arial', 9), 
                                     background='#34495e', foreground='white')
        self.status_label.pack(fill='x', side='bottom')
        
        # 데이터 저장용
        self.scraped_data = []
        
    def start_scraping(self):
        url = self.url_entry.get().strip()
        selector = self.selector_entry.get().strip()
        
        if not url or not selector:
            messagebox.showwarning("Input Required", "Please enter both URL and CSS selector")
            return
        
        # 버튼 비활성화
        self.scrape_btn.config(state='disabled', text="Scraping...")
        self.status_label.config(text="Scraping in progress...")
        self.result_text.delete(1.0, tk.END)
        
        # 별도 스레드에서 스크래핑 실행
        thread = threading.Thread(target=self.scrape, args=(url, selector))
        thread.daemon = True
        thread.start()
        
    def scrape(self, url, selector):
        try:
            # HTTP 요청
            self.update_status("Fetching webpage...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # HTML 파싱
            self.update_status("Parsing HTML...")
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.select(selector)
            
            if not elements:
                self.update_result("❌ No elements found with selector: " + selector)
                self.scrape_btn.config(state='normal', text="🚀 Start Scraping")
                self.status_label.config(text="No results found")
                return
            
            # 데이터 추출
            self.scraped_data = []
            result_text = f"✅ Found {len(elements)} elements\n"
            result_text += "=" * 60 + "\n\n"
            
            for idx, elem in enumerate(elements, 1):
                data = {'index': idx}
                
                if self.extract_text_var.get():
                    text = elem.get_text(strip=True)
                    data['text'] = text
                    result_text += f"[{idx}] Text: {text}\n"
                
                if self.extract_links_var.get():
                    link = elem.get('href', '')
                    if link:
                        data['link'] = link
                        result_text += f"    Link: {link}\n"
                
                result_text += "\n"
                self.scraped_data.append(data)
            
            self.update_result(result_text)
            self.update_status(f"✅ Successfully scraped {len(elements)} items")
            
            # Export 버튼 활성화
            self.root.after(0, lambda: self.export_csv_btn.config(state='normal'))
            self.root.after(0, lambda: self.export_json_btn.config(state='normal'))
            
        except requests.exceptions.RequestException as e:
            self.update_result(f"❌ Network Error: {str(e)}")
            self.update_status("Error occurred")
        except Exception as e:
            self.update_result(f"❌ Error: {str(e)}")
            self.update_status("Error occurred")
        finally:
            self.root.after(0, lambda: self.scrape_btn.config(state='normal', text="🚀 Start Scraping"))
    
    def update_result(self, text):
        def update():
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, text)
        self.root.after(0, update)
    
    def update_status(self, text):
        self.root.after(0, lambda: self.status_label.config(text=text))
    
    def export_csv(self):
        if not self.scraped_data:
            messagebox.showwarning("No Data", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    if self.scraped_data:
                        writer = csv.DictWriter(f, fieldnames=self.scraped_data[0].keys())
                        writer.writeheader()
                        writer.writerows(self.scraped_data)
                
                messagebox.showinfo("Success", f"Data exported to:\n{filename}")
                self.status_label.config(text=f"✅ Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
    
    def export_json(self):
        if not self.scraped_data:
            messagebox.showwarning("No Data", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Data exported to:\n{filename}")
                self.status_label.config(text=f"✅ Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperTool(root)
    root.mainloop()