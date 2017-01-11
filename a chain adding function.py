# add(1)(2)(3); // 6
# add(1)(2)(3)(4); // 10
# add(1)(2)(3)(4)(5); // 15

# на основе
# http://stackoverflow.com/questions/39038358/function-chaining-in-python
# черт возьми, это красиво
# мы ПРОСТО переопределяем поведение объекта класса int, позволяя его ВЫЗЫВАТЬ
# охуительно

class add(int):
    def __call__(self,v):
        return add(self+v)

