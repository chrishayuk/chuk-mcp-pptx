#!/usr/bin/env python3
"""
Code Examples Demo for PowerPoint MCP Server

Demonstrates code blocks in presentations with syntax highlighting.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from chuk_mcp_pptx.server import (
    pptx_create,
    pptx_add_slide,
    pptx_save,
    pptx_apply_theme,
    pptx_add_code_block,
    pptx_add_shape,
)


async def create_code_examples():
    """Create presentation with various code examples."""

    print("\n💻 PowerPoint MCP Server - Code Examples")
    print("=" * 70)
    print("📝 Creating Code Examples Presentation")
    print("=" * 60)

    # Create presentation
    print("\n1. Creating presentation...")
    await pptx_create("code_examples")

    # Apply dark theme for better code visibility
    print("2. Applying dark theme...")
    await pptx_apply_theme(theme="dark_purple")

    # Title slide
    print("3. Creating title slide...")
    await pptx_add_slide(
        title="Code Examples Showcase",
        content=[
            "Beautiful code blocks in presentations",
            "Multiple programming languages",
            "Syntax highlighting appearance",
            "Dark theme optimized",
        ],
    )

    # Python example
    print("\n4. Adding Python code example...")
    await pptx_add_slide(title="Python Example", content=[])

    python_code = """def fibonacci(n):
    \"\"\"Generate Fibonacci sequence up to n terms.\"\"\"
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    
    return sequence

# Example usage
result = fibonacci(10)
print(f"Fibonacci sequence: {result}")"""

    await pptx_add_code_block(
        slide_index=1,
        code=python_code,
        language="python",
        left=1.0,
        top=1.8,
        width=8.0,
        height=3.5,
        theme="dark_purple",
    )

    # JavaScript example
    print("5. Adding JavaScript code example...")
    await pptx_add_slide(title="JavaScript Example", content=[])

    js_code = """// React component with hooks
import React, { useState, useEffect } from 'react';

const DataFetcher = ({ apiUrl }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(apiUrl);
                const json = await response.json();
                setData(json);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        
        fetchData();
    }, [apiUrl]);
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    return <div>{JSON.stringify(data)}</div>;
};"""

    await pptx_add_code_block(
        slide_index=2,
        code=js_code,
        language="javascript",
        left=0.5,
        top=1.8,
        width=9.0,
        height=4.0,
        theme="dark_blue",
    )

    # SQL example
    print("6. Adding SQL code example...")
    await pptx_add_slide(title="SQL Query Example", content=[])

    sql_code = """-- Complex query with CTEs and window functions
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        product_id,
        SUM(quantity * unit_price) AS revenue,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    WHERE order_date >= '2024-01-01'
    GROUP BY 1, 2
),
ranked_products AS (
    SELECT 
        month,
        product_id,
        revenue,
        unique_customers,
        ROW_NUMBER() OVER (PARTITION BY month ORDER BY revenue DESC) AS rank
    FROM monthly_sales
)
SELECT 
    month,
    product_id,
    revenue,
    unique_customers,
    LAG(revenue) OVER (PARTITION BY product_id ORDER BY month) AS prev_revenue,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (PARTITION BY product_id ORDER BY month)) / 
          NULLIF(LAG(revenue) OVER (PARTITION BY product_id ORDER BY month), 0), 2) AS growth_pct
FROM ranked_products
WHERE rank <= 5
ORDER BY month, rank;"""

    await pptx_add_code_block(
        slide_index=3,
        code=sql_code,
        language="sql",
        left=0.5,
        top=1.8,
        width=9.0,
        height=4.0,
        theme="dark_green",
    )

    # Rust example
    print("7. Adding Rust code example...")
    await pptx_add_slide(title="Rust System Programming", content=[])

    rust_code = """use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

#[derive(Debug)]
struct Counter {
    value: i32,
}

impl Counter {
    fn new() -> Self {
        Counter { value: 0 }
    }
    
    fn increment(&mut self) {
        self.value += 1;
    }
}

fn main() {
    let counter = Arc::new(Mutex::new(Counter::new()));
    let mut handles = vec![];
    
    for i in 0..10 {
        let counter_clone = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter_clone.lock().unwrap();
            num.increment();
            println!("Thread {} incremented counter", i);
            thread::sleep(Duration::from_millis(10));
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("Final counter: {:?}", *counter.lock().unwrap());
}"""

    await pptx_add_code_block(
        slide_index=4,
        code=rust_code,
        language="rust",
        left=0.5,
        top=1.8,
        width=9.0,
        height=4.0,
        theme="dark_modern",
    )

    # Mixed slide with code and explanation
    print("8. Adding mixed content slide...")
    await pptx_add_slide(title="API Design Pattern", content=[])

    # Add explanation shape
    await pptx_add_shape(
        slide_index=5,
        shape_type="rounded_rectangle",
        left=0.5,
        top=1.8,
        width=4.0,
        height=1.0,
        text="RESTful API with authentication",
    )

    # Add code
    api_code = """from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

@app.post("/users/")
async def create_user(user: User):
    # Validate and create user
    return {"id": 123, **user.dict()}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Fetch user from database
    return {"id": user_id, "username": "john"}"""

    await pptx_add_code_block(
        slide_index=5,
        code=api_code,
        language="python",
        left=0.5,
        top=3.0,
        width=9.0,
        height=2.5,
        theme="cyberpunk",
    )

    # Docker example
    print("9. Adding Docker configuration example...")
    await pptx_add_slide(title="Container Configuration", content=[])

    docker_code = """# Multi-stage Docker build for Python app
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim AS runner

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]"""

    await pptx_add_code_block(
        slide_index=6,
        code=docker_code,
        language="dockerfile",
        left=1.0,
        top=2.0,
        width=8.0,
        height=3.5,
        theme="dark_blue",
    )

    # Summary slide
    print("10. Adding summary slide...")
    await pptx_add_slide(
        title="Code in Presentations",
        content=[
            "✅ Multiple programming languages supported",
            "✅ Dark themes for better readability",
            "✅ Monospace fonts for code clarity",
            "✅ Language labels for context",
            "✅ Customizable size and positioning",
            "✅ Perfect for technical presentations",
        ],
    )

    # Save presentation
    print("\n11. Saving presentation...")
    await pptx_save("../outputs/code_examples.pptx")
    print("   ✅ Saved to outputs/code_examples.pptx")

    print("\n" + "=" * 60)
    print("🎉 Code Examples presentation created successfully!")
    print("📁 File saved as: outputs/code_examples.pptx")
    print("\n💡 Features demonstrated:")
    print("   • Python, JavaScript, SQL, Rust code examples")
    print("   • Docker configuration")
    print("   • FastAPI example")
    print("   • Different themes for each code block")
    print("   • Mixed content (code + explanations)")
    print("\n🎨 Themes used:")
    print("   • dark_purple, dark_blue, dark_green")
    print("   • dark_modern, cyberpunk")


async def main():
    """Main execution function."""
    await create_code_examples()

    print("\n" + "=" * 70)
    print("📚 Use cases for code in presentations:")
    print("   1. Technical documentation")
    print("   2. Code reviews and walkthroughs")
    print("   3. Programming tutorials")
    print("   4. API documentation")
    print("   5. Architecture discussions")
    print("   6. Bug reports and fixes")
    print("   7. Best practices demonstrations")
    print("\n💼 Perfect for:")
    print("   • Developer meetings")
    print("   • Technical training")
    print("   • Conference talks")
    print("   • Code bootcamps")
    print("   • Engineering reviews")


if __name__ == "__main__":
    asyncio.run(main())
