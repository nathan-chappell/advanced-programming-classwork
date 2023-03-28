#include <stdio.h>
#include <stdlib.h>


struct Object;

void *Object_id(struct Object *object)
{
    return object;
}

void Object_print(struct Object *object)
{
    printf("<Object addr=%p>\n", object);
}

struct ObjectVTable
{
    void *(*id)(struct Object *);
    void (*print)(struct Object *);
};

struct ObjectVTable *objectVTable = NULL;

void init_object_vtable()
{
    if (objectVTable == NULL)
    {
        objectVTable = malloc(sizeof(struct ObjectVTable));
        objectVTable->id = Object_id;
        objectVTable->print = Object_print;
    }
}

struct Object
{
    struct ObjectVTable *vtable;
};

struct IntObject;

void IntObject_print(struct IntObject *intObject);
struct IntObject *IntObject_add(struct IntObject *l, struct IntObject *r);

struct IntVTable
{
    struct ObjectVTable objectVTable;
    struct IntObject *(*add)(struct IntObject *l, struct IntObject *r);
};

struct IntVTable *intVTable = NULL;

void init_int_vtable()
{
    if (intVTable == NULL)
    {
        intVTable = malloc(sizeof(struct IntVTable));
        intVTable->objectVTable.print = IntObject_print;
        intVTable->add = IntObject_add;
    }
}

struct IntObject
{
    struct IntVTable *vtable;
    int value;
};

struct IntObject *IntObject_Construct(int value)
{
    struct IntObject *object = malloc(sizeof(struct IntObject));
    object->vtable = intVTable;
    object->value = value;
    return object;
}

void IntObject_print(struct IntObject *intObject)
{
    printf("<IntObject val=%d>\n", intObject->value);
}

struct IntObject *IntObject_add(struct IntObject *l, struct IntObject *r)
{
    struct IntObject *result = IntObject_Construct(l->value);
    result->value += r->value;
    return result;
}

void init_vtables()
{
    init_object_vtable();
    init_int_vtable();
}

int main(int argc, char **argv)
{
    init_vtables();
    struct IntObject *three = IntObject_Construct(3);
    struct IntObject *four = IntObject_Construct(4);
    three->vtable->objectVTable.print(three);
    four->vtable->objectVTable.print(four);
    struct IntObject *seven = three->vtable->add(three, four);
    seven->vtable->objectVTable.print(seven);
}