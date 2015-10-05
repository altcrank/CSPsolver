class Different:
    def two_domains(self, domain1, domain2):
        if len(domain1) == 1:
            for value in domain1:
                domain2.discard(value)
                
        if len(domain2) == 1:
            for value in domain2:
                domain1.discard(value)
    
    def __call__(self, domains):
        if len(domains) < 2:
            return
        
        sorted_domains = sorted(domains, key=lambda dom: len(dom))
        for domain1 in sorted_domains:
            if len(domain1) > 1:
                break
            for domain2 in sorted_domains:
                if domain1 is not domain2:
                    self.two_domains(domain1, domain2)  

domain1 = {1}
domain2 = {2}
domain3 = {2, 5}
domain4 = {1, 2, 3}
domain5 = {3, 4, 5}
domain6 = {3, 6, 7}

diff = Different()
diff([domain1, domain2])
print domain1, domain2
diff([domain2, domain3])
print domain2, domain3
diff([domain1, domain2, domain4, domain5, domain6])
print domain4, domain5, domain6
