import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Check, HelpCircle } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function PricingPage() {
  return (
    <div className="container max-w-6xl py-10">
      <div className="flex flex-col space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl">Pricing Plans</h1>
          <p className="max-w-2xl mx-auto text-xl text-muted-foreground">
            Choose the perfect plan for your freelancing journey
          </p>
        </div>

        <div className="flex justify-center">
          <Tabs defaultValue="monthly" className="w-full max-w-md">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="monthly">Monthly</TabsTrigger>
              <TabsTrigger value="annual">Annual (Save 20%)</TabsTrigger>
            </TabsList>
        
            <TabsContent value="monthly" className="mt-8 flex justify-center">
              <div className="grid gap- md:grid-cols-3 justify-center w-full ">
                <Card className="border-2 w-72">
                  <CardHeader className="space-y-1 ">
                    <CardTitle className="text-2xl">Free</CardTitle>
                    <CardDescription>Get started with basic freelancing tools</CardDescription>
                    <div className="pt-2">
                      <span className="text-3xl font-bold">$0</span>
                      <span className="text-muted-foreground ml-1">/month</span>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Create up to 3 active gigs</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Basic analytics dashboard</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Community forum access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Limited blog access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Manual gig publishing</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button variant="outline" className="w-full" asChild>
                      <Link href="/signup">Get Started</Link>
                    </Button>
                  </CardFooter>
                </Card>

                <Card className="border-2 border-primary relative w-72">
                  <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-0">
                    <Badge className="bg-primary text-primary-foreground">Popular</Badge>
                  </div>
                  <CardHeader className="space-y-1 ">
                    <CardTitle className="text-2xl">Pro</CardTitle>
                    <CardDescription>Perfect for active freelancers</CardDescription>
                    <div className="pt-2">
                      <span className="text-3xl font-bold">$19</span>
                      <span className="text-muted-foreground ml-1">/month</span>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Create up to 15 active gigs</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Advanced analytics & insights</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Priority community support</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Full blog access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Auto-publish to 2 platforms</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>AI-powered gig optimization</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Custom profile showcase</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button className="w-full" asChild>
                      <Link href="/signup?plan=pro">Get Started</Link>
                    </Button>
                  </CardFooter>
                </Card>

                <Card className="border-2 w-72">
                  <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl">Business</CardTitle>
                    <CardDescription>For power users and small agencies</CardDescription>
                    <div className="pt-2">
                      <span className="text-3xl font-bold">$49</span>
                      <span className="text-muted-foreground ml-1">/month</span>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Unlimited active gigs</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Enterprise analytics suite</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Dedicated account manager</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Premium blog & resource access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Auto-publish to all platforms</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Advanced AI business insights</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Team collaboration tools</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Client CRM integration</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button variant="outline" className="w-full" asChild>
                      <Link href="/signup?plan=business">Get Started</Link>
                    </Button>
                  </CardFooter>
                </Card>
              </div>
            </TabsContent>
          
            <TabsContent value="annual" className="mt-4 flex justify-center">
              <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3 w-full max-w-5xl">
                <Card className="border-2">
                  <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl">Free</CardTitle>
                    <CardDescription>Get started with basic freelancing tools</CardDescription>
                    <div className="pt-2">
                      <span className="text-3xl font-bold">$0</span>
                      <span className="text-muted-foreground ml-1">/year</span>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Create up to 3 active gigs</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Basic analytics dashboard</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Community forum access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Limited blog access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Manual gig publishing</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button variant="outline" className="w-full" asChild>
                      <Link href="/signup">Get Started</Link>
                    </Button>
                  </CardFooter>
                </Card>

                <Card className="border-2 border-primary relative">
                  <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-0">
                    <Badge className="bg-primary text-primary-foreground">Popular</Badge>
                  </div>
                  <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl">Pro</CardTitle>
                    <CardDescription>Perfect for active freelancers</CardDescription>
                    <div className="pt-2">
                      <span className="text-3xl font-bold">$15</span>
                      <span className="text-muted-foreground ml-1">/month</span>
                      <div className="text-sm text-muted-foreground mt-1">Billed annually ($180)</div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Create up to 15 active gigs</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Advanced analytics & insights</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Priority community support</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Full blog access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Auto-publish to 2 platforms</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>AI-powered gig optimization</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Custom profile showcase</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button className="w-full" asChild>
                      <Link href="/signup?plan=pro-annual">Get Started</Link>
                    </Button>
                  </CardFooter>
                </Card>

                <Card className="border-2">
                  <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl">Business</CardTitle>
                    <CardDescription>For power users and small agencies</CardDescription>
                    <div className="pt-2">
                      <span className="text-3xl font-bold">$39</span>
                      <span className="text-muted-foreground ml-1">/month</span>
                      <div className="text-sm text-muted-foreground mt-1">Billed annually ($468)</div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Unlimited active gigs</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Enterprise analytics suite</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Dedicated account manager</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Premium blog & resource access</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Auto-publish to all platforms</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Advanced AI business insights</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Team collaboration tools</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Check className="h-4 w-4 text-primary" />
                        <span>Client CRM integration</span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button variant="outline" className="w-full" asChild>
                      <Link href="/signup?plan=business-annual">Get Started</Link>
                    </Button>
                  </CardFooter>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>

        <div className="space-y-8 mt-12">
          <h2 className="text-3xl font-bold text-center">Feature Comparison</h2>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b">
                  <th className="py-4 px-6 text-left">Feature</th>
                  <th className="py-4 px-6 text-center">Free</th>
                  <th className="py-4 px-6 text-center">Pro</th>
                  <th className="py-4 px-6 text-center">Business</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">Active Gigs</td>
                  <td className="py-4 px-6 text-center">3</td>
                  <td className="py-4 px-6 text-center">15</td>
                  <td className="py-4 px-6 text-center">Unlimited</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">
                    <div className="flex items-center gap-1">
                      <span>Analytics</span>
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger>
                            <HelpCircle className="h-4 w-4 text-muted-foreground" />
                          </TooltipTrigger>
                          <TooltipContent>
                            <p className="w-[200px] text-sm">Track your performance, earnings, and client engagement</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </div>
                  </td>
                  <td className="py-4 px-6 text-center">Basic</td>
                  <td className="py-4 px-6 text-center">Advanced</td>
                  <td className="py-4 px-6 text-center">Enterprise</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">Platform Publishing</td>
                  <td className="py-4 px-6 text-center">Manual</td>
                  <td className="py-4 px-6 text-center">2 platforms</td>
                  <td className="py-4 px-6 text-center">All platforms</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">AI Optimization</td>
                  <td className="py-4 px-6 text-center">—</td>
                  <td className="py-4 px-6 text-center">Basic</td>
                  <td className="py-4 px-6 text-center">Advanced</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">Support</td>
                  <td className="py-4 px-6 text-center">Community</td>
                  <td className="py-4 px-6 text-center">Priority</td>
                  <td className="py-4 px-6 text-center">Dedicated</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">Team Members</td>
                  <td className="py-4 px-6 text-center">1</td>
                  <td className="py-4 px-6 text-center">1</td>
                  <td className="py-4 px-6 text-center">Up to 5</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">Client Management</td>
                  <td className="py-4 px-6 text-center">Basic</td>
                  <td className="py-4 px-6 text-center">Advanced</td>
                  <td className="py-4 px-6 text-center">CRM Integration</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-6 font-medium">Custom Branding</td>
                  <td className="py-4 px-6 text-center">—</td>
                  <td className="py-4 px-6 text-center">Limited</td>
                  <td className="py-4 px-6 text-center">Full</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-muted rounded-lg p-8 mt-8">
          <div className="flex flex-col lg:flex-row items-center justify-between gap-6">
            <div className="space-y-4 text-center lg:text-left">
              <h2 className="text-2xl font-bold">Need a custom plan for your agency?</h2>
              <p className="text-muted-foreground">
                Contact our sales team for a customized solution that fits your specific needs.
              </p>
            </div>
            <Button size="lg" className="px-8" asChild>
              <Link href="/contact">Contact Sales</Link>
            </Button>
          </div>
        </div>

        <div className="space-y-6 mt-8">
          <h2 className="text-3xl font-bold text-center">Frequently Asked Questions</h2>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle className="text-xl">How does billing work?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  You'll be billed monthly or annually depending on your chosen plan. You can upgrade, downgrade, or
                  cancel your subscription at any time.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-xl">Can I switch plans later?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Yes, you can upgrade or downgrade your plan at any time. If you upgrade, you'll be charged the
                  prorated difference. If you downgrade, you'll receive credit toward your next billing cycle.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-xl">Is there a free trial?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Yes, all paid plans include a 14-day free trial. No credit card is required to start your trial.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-xl">What payment methods do you accept?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  We accept all major credit cards, PayPal, and in some regions, bank transfers for annual plans.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-xl">Can I cancel anytime?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Yes, you can cancel your subscription at any time. If you cancel, you'll continue to have access until
                  the end of your current billing period.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-xl">Do you offer discounts?</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  We offer a 20% discount for annual billing. We also have special rates for educational institutions
                  and non-profit organizations.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

