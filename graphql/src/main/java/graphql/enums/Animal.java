package graphql.enums;

// this can have values that don't match the definition in the .graphqls file,
// but it will throw an error if you try to return a value with it
public enum Animal {
	DOG, CAT, BADGER, MAMMOTH, ANOTHER_ANIMAL
}