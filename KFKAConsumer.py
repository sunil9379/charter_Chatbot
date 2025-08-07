//
import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Head from "next/head";
import Link from "next/link";
import { useRouter } from "next/router";
const products = [
{
category: "Watches",
items: [
{ slug: "gmt-masters", name: "GMT Masters", description: "Luxury GMT watches for
travelers.", price: "$199" },
],
},
{
category: "Apparels",
items: [
{ slug: "wide-leg-linen-pants-women", name: "Wide Leg Linen Pants Women", description:
"Breathable, stylish summer wear.", price: "$49" },
],
},
{
category: "Footwear",
items: [
{ slug: "casual-sneakers", name: "Casual Sneakers", description: "Everyday comfort and
style.", price: "$79" },
],
},
{
category: "Home Decor",
items: [
{ slug: "coastal-home-decor", name: "Coastal Home Decor", description: "Bring the seaside
feel home.", price: "$129" },
],
},
{
category: "Skincare",
items: [
{ slug: "night-serums", name: "Night Serums", description: "Revitalize your skin overnight.",
price: "$39" },
],
},
];
export default function HomePage() {
return (
<div className="p-6">
<Head>
<title>Shop Luxury Watches, Apparel, Home Decor | Trendy Online Store</title>
<meta name="description" content="Buy GMT Masters, Wide Leg Linen Pants, Night
Serums, and Coastal Home Decor online. Top quality products for USA, UK, Canada, and
India." />
<meta name="keywords" content="GMT Masters, Wide Leg Linen Pants Women, Coastal
Home Decor, Night Serums, Luxury Watches, Skincare, Footwear" />
<script
type="application/ld+json"
dangerouslySetInnerHTML={{
__html: JSON.stringify({
"@context": "https://schema.org",
"@type": "Store",
"name": "Trendy Online Store",
"description": "Premium lifestyle products including watches, apparel, footwear, home
decor, and skincare.",
"url": "https://yourstore.com",
"potentialAction": {
"@type": "SearchAction",
"target": "https://yourstore.com/search?q={search_term_string}",
"query-input": "required name=search_term_string"
},
}),
}}
/>
</Head>
<h1 className="text-4xl font-bold mb-4">Discover Premium Lifestyle Products</h1>
{products.map((category, idx) => (
<div key={idx} className="mb-8">
<h2 className="text-2xl font-semibold mb-2">{category.category}</h2>
<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
{category.items.map((item, i) => (
<Card key={i} className="rounded-2xl shadow-md">
<CardContent className="p-4">
<h3 className="text-xl font-medium mb-1">
<Link href={`/product/${item.slug}`} className="text-blue-600 hover:underline">
{item.name}
</Link>
</h3>
<p className="text-gray-600 mb-2">{item.description}</p>
<p className="text-lg font-bold mb-3">{item.price}</p>
<Button>Add to Cart</Button>
</CardContent>
</Card>
))}
</div>
</div>
))}
</div>
);
}
/